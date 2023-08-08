import dns.resolver


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
