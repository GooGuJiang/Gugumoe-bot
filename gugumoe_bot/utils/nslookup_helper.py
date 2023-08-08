import ipaddress
import re

import dns.resolver


def identify_and_extract_ip(input_str):
    # Patterns
    ipv4_pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
    ipv6_pattern = r'^(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}$'
    domain_pattern = r'^[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?$'
    url_pattern = r'https?://([\w\-\.]+)/?'

    # Check IPv4
    if re.match(ipv4_pattern, input_str):
        ip = ipaddress.ip_address(input_str)
        if ip.is_loopback:
            return "Loopback", input_str
        elif ip.is_private:
            return "Private", input_str
        else:
            return "IPv4", input_str

    # Check IPv6
    if re.match(ipv6_pattern, input_str):
        ip = ipaddress.ip_address(input_str)
        if ip.is_loopback:
            return "Loopback", input_str
        elif ip.is_private:
            return "Private", input_str
        else:
            return "IPv6", input_str

    # Check URL
    match = re.match(url_pattern, input_str)
    if match:
        domain = match.group(1)
        if re.match(domain_pattern, domain):
            return "Domain", domain

    # Check Domain
    if re.match(domain_pattern, input_str):
        return "Domain", input_str

    return "Unknown", None


def get_records(domain, nameserver="8.8.8.8"):
    # 创建一个解析器实例
    resolver = dns.resolver.Resolver()

    # 指定DNS服务器
    resolver.nameservers = [nameserver]

    # 定义字典用来保存解析结果
    records = {'A': [], 'AAAA': []}

    for record_type in ['A', 'AAAA']:
        try:
            # 使用resolver.resolve进行解析
            answers = resolver.resolve(domain, record_type)
            for rdata in answers:
                records[record_type].append(rdata.to_text())
        except dns.resolver.NoAnswer:
            print(f"No {record_type} record found for {domain}")
        except dns.resolver.NXDOMAIN:
            print(f"Domain {domain} does not exist")
            break
    return records


if __name__ == '__main__':
    print(get_records('www.gmoe.cc', '1.1.1.1'))  # 使用Google的公共DNS服务器
