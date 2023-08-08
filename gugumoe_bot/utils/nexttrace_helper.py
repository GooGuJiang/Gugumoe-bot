import math
import os
import platform
import subprocess
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from loguru import logger

# 获取当前文件上一级目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_nexttrace_output(output):
    lines = output.strip().split('\n')[4:]  # skip the header lines
    hops = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line:
            parts = line.split()

            # Check if line is a hop (starts with a number) or a response time
            if parts[0].isdigit():
                # Initialize a basic hop dictionary
                hop = {
                    "number": int(parts[0]),
                    "ip": parts[1],
                }

                # Fill in additional information if available
                if len(parts) > 2:
                    hop["as_number"] = parts[2] if "AS" in parts[2] else None
                    hop["location"] = " ".join(parts[3:-1]) if len(parts) > 3 else None
                    hop["website"] = parts[-1] if "." in parts[-1] else None

                # If the next line contains response time
                if i + 1 < len(lines) and "ms" in lines[i + 1]:
                    i += 1
                    hop["response_times"] = lines[i].strip()

                hops.append(hop)

        i += 1

    return hops


def run_traceroute(host):
    """Runs the nexttrace command and returns the output as a string."""
    current_os = platform.system().lower()

    # 根据操作系统来确定使用哪个命令
    if current_os == 'windows':
        cmd = ['nexttrace', '--map=false', '-q', '1', '--send-time', '1', host]
    elif current_os == 'linux':
        cmd = ['nexttrace', '--map=false', '-q', '1', '--send-time', '1', host]
    else:
        logger.error(f"Unsupported platform: {current_os}")
        return

    # 使用subprocess.Popen来执行命令
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
                               encoding='utf-8')

    results = ''

    # 读取子进程的输出
    for line in iter(process.stdout.readline, ''):
        line = line.strip()  # 去除行尾的 \n
        # 组合成文本
        results += line + '\n'

    return results


class NextTraceHelper:

    def __init__(self):
        self.colors = {
            "number": "#fdc47d",
            "ip": "#d2549a",
            "as_number": "#3ed7b9",
            "as_number_asterisk": "#1fb065",
            "location": "#e2e3e8",
            "response_times_text": "#8d91a5",
            "response_times": "#44a7ff",
            "asterisk": "#e2e3e8",
            "website": "#1bb568",
            "bg": "#141729"
        }

    def nexttrace_generate_image(self, json_list):
        def draw_colored_text(draw, x, y, text, key, font):
            color = self.colors.get(key, "black")
            draw.text((x, y), text, font=font, fill=color)
            return font.getlength(text)

        font_size = 20
        font = ImageFont.truetype(f"{BASE_DIR}/fonts/Sarasa-Mono-SC-Semibold-Nerd.ttf", font_size)
        bold_font = ImageFont.truetype(f"{BASE_DIR}/fonts/Sarasa-Mono-SC-Bold-Nerd.ttf", font_size)
        # 计算每一项的最大宽度
        number_width = max([bold_font.getlength("{:<4}".format(item["number"])) for item in json_list])
        ip_width = max([bold_font.getlength(item["ip"]) for item in json_list])
        as_number_width = max([bold_font.getlength(item.get("as_number") or "*") for item in json_list])
        location_width = max([bold_font.getlength(item.get("location", "")) for item in json_list])
        website_width = max([font.getlength(item.get("website") or "") for item in json_list])
        response_times_width = max([bold_font.getlength(item.get("response_times", "")) for item in json_list])

        # 根据最大宽度来计算整个图片的最大宽度
        max_width = 10 + number_width + ip_width + as_number_width + location_width + website_width + response_times_width / 4

        max_width = math.ceil(max_width) + 20  # 加上左右的间距
        ip_width = max([bold_font.getlength("{:<15}".format(item["ip"])) for item in json_list])

        # 绘制每一行
        lines = []
        for item in json_list:
            image = Image.new('RGB', (max_width, font_size * 4), color=self.colors["bg"])  # 设置为4倍的字体高度
            draw = ImageDraw.Draw(image)

            x = 10
            y = 10

            x += draw_colored_text(draw, x, y, "{:<4}".format(item["number"]), "number", bold_font)
            x += draw_colored_text(draw, x, y, "{:<16}".format(item["ip"]), "ip", bold_font)
            x += draw_colored_text(draw, x, y, "{:<10}".format(item.get("as_number") or "*"), "as_number", bold_font)
            x += draw_colored_text(draw, x, y, "{:<40}".format(item.get("location", "")), "location", bold_font)
            x += draw_colored_text(draw, x, y, "{:<10}".format(item.get("website") or ""), "website", font)

            align_x = ip_width + as_number_width + location_width + website_width + 150  # 对齐的x坐标
            # 移动response_times到下一行，并与ip对齐
            if len(item.get("response_times", "").split(" ")) >= 3:
                # x = align_x - font.getlength(item.get("response_times", ""))
                y += font_size + 10  # 移动到下一行
                response_times_ms = item.get("response_times", "").split(" ", 1)[1]
                response_times_text = item.get("response_times", "").split(" ", 1)[0]
                x_1 = align_x - font.getlength(response_times_ms)
                draw_colored_text(draw, x_1, y, response_times_ms, "response_times", bold_font)
                draw_colored_text(draw, 50, y, response_times_text, "response_times_text", bold_font)
            else:
                x = align_x - font.getlength(item.get("response_times", ""))
                y += font_size + 10  # 移动到下一行
                draw_colored_text(draw, x, y, item.get("response_times", ""), "response_times", bold_font)
            lines.append(image)

        # 合并图像
        final_height = sum([img.height for img in lines])
        final_image = Image.new('RGB', (max_width, final_height), color=self.colors["bg"])

        y_offset = 0
        for img in lines:
            final_image.paste(img, (0, y_offset))
            y_offset += img.height

        img_byte_array = BytesIO()
        final_image.save(img_byte_array, format='PNG')
        return img_byte_array.getvalue()

    def execute_and_generate_image(self, host):
        results = run_traceroute(host)
        hops = parse_nexttrace_output(results)
        return self.nexttrace_generate_image(hops)


if __name__ == '__main__':
    helper = NextTraceHelper()
    img_bytes = helper.execute_and_generate_image("127.0.0.1")
    with open("traceroute_result.png", "wb") as f:
        f.write(img_bytes)
