from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
def add_utm_params(from_url, to_url):
    """
    根据来源链接和目标链接，生成带有固定UTM参数的目标链接
    
    参数:
        from_url (str): 来源链接，例如 "https://mp.jobleap4u.com/"
        to_url (str): 目标链接，例如 "https://jobleap.cn/"
    
    返回:
        str: 带有UTM参数的目标链接，格式如：
             https://jobleap.cn/?utm_source=mp_jobleap4u&utm_medium=discover_page&utm_campaign=content_cta
    """
    # 1. 从来源链接提取utm_source（取域名主体，替换点为下划线）
    parsed_from = urlparse(from_url)
    # 提取域名（如 mp.jobleap4u.com → 取 mp.jobleap4u）
    domain_parts = parsed_from.netloc.split('.')
    # 排除最后的顶级域名（如 .com, .cn），取前面的部分作为source
    source_parts = domain_parts[:-1] if len(domain_parts) > 1 else domain_parts
    utm_source = '_'.join(source_parts)
    
    # 2. 固定UTM参数
    utm_medium = "discover_page"
    utm_campaign = "content_cta"
    
    # 3. 解析目标链接，添加UTM参数
    parsed_to = urlparse(to_url)
    # 获取现有查询参数
    query_params = parse_qs(parsed_to.query)
    
    # 添加UTM参数（覆盖已有同名参数，确保统计准确性）
    query_params['utm_source'] = [utm_source]
    query_params['utm_medium'] = [utm_medium]
    query_params['utm_campaign'] = [utm_campaign]
    
    # 重建查询字符串
    new_query = urlencode(query_params, doseq=True)
    
    # 重建完整URL
    return urlunparse(parsed_to._replace(query=new_query))


# 测试示例
if __name__ == "__main__":
    # 测试案例1：基础链接
    from_url1 = "https://github.com/XiaomingX/utm-generator-dev"
    to_url1 = "https://jobleap.cn/"
    result1 = add_utm_params(from_url1, to_url1)
    print(f"来源链接: {from_url1}")
    print(f"目标链接: {to_url1}")
    print(f"带UTM的链接: {result1}\n")  # 预期包含 utm_source=mp_jobleap4u
    
    # 测试案例2：目标链接已有其他参数
    # from_url2 = "https://mp.jobleap4u.com/discover"
    # to_url2 = "https://jobleap.cn/jobs?type=fulltime"
    # result2 = add_utm_params(from_url2, to_url2)
    # print(f"来源链接: {from_url2}")
    # print(f"目标链接: {to_url2}")
    # print(f"带UTM的链接: {result2}")  # 保留原有type参数，新增UTM参数
    