from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

# 原有函数保持不变
def add_utm_params(from_url, to_url):
    """
    根据来源链接和目标链接，生成带有固定UTM参数的目标链接
    
    参数:
        from_url (str): 来源链接，例如 "https://mp.jobleap4u.com/"
        to_url (str): 目标链接，例如 "https://jobleap.cn/"
    
    返回:
        str: 带有UTM参数的目标链接
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


# 补充函数1：允许自定义utm_medium和utm_campaign
def add_custom_utm_params(from_url, to_url, utm_medium, utm_campaign):
    """
    生成带有自定义utm_medium和utm_campaign的目标链接
    
    参数:
        from_url (str): 来源链接
        to_url (str): 目标链接
        utm_medium (str): 自定义的媒介参数（如 "email"、"social"）
        utm_campaign (str): 自定义的活动参数（如 "2023_sale"）
    
    返回:
        str: 带有自定义UTM参数的目标链接
    """
    # 复用来源提取逻辑
    parsed_from = urlparse(from_url)
    domain_parts = parsed_from.netloc.split('.')
    source_parts = domain_parts[:-1] if len(domain_parts) > 1 else domain_parts
    utm_source = '_'.join(source_parts)
    
    # 解析目标链接
    parsed_to = urlparse(to_url)
    query_params = parse_qs(parsed_to.query)
    
    # 添加自定义参数（覆盖已有）
    query_params['utm_source'] = [utm_source]
    query_params['utm_medium'] = [utm_medium]
    query_params['utm_campaign'] = [utm_campaign]
    
    new_query = urlencode(query_params, doseq=True)
    return urlunparse(parsed_to._replace(query=new_query))


# 补充函数2：处理缺少协议的来源链接（自动补充http协议）
def add_utm_from_incomplete_url(from_url, to_url):
    """
    处理来源链接缺少http/https协议的情况（如 "mp.jobleap4u.com"）
    
    参数:
        from_url (str): 可能缺少协议的来源链接
        to_url (str): 目标链接
    
    返回:
        str: 带有UTM参数的目标链接
    """
    # 检查并补充协议
    parsed_from = urlparse(from_url)
    if not parsed_from.scheme:  # 无协议时补充http
        from_url = f"http://{from_url}"
        parsed_from = urlparse(from_url)
    
    # 复用来源提取逻辑
    domain_parts = parsed_from.netloc.split('.')
    source_parts = domain_parts[:-1] if len(domain_parts) > 1 else domain_parts
    utm_source = '_'.join(source_parts)
    
    # 固定参数（同原有函数）
    utm_medium = "discover_page"
    utm_campaign = "content_cta"
    
    # 处理目标链接
    parsed_to = urlparse(to_url)
    query_params = parse_qs(parsed_to.query)
    query_params['utm_source'] = [utm_source]
    query_params['utm_medium'] = [utm_medium]
    query_params['utm_campaign'] = [utm_campaign]
    
    new_query = urlencode(query_params, doseq=True)
    return urlunparse(parsed_to._replace(query=new_query))


# 补充函数3：从来源链接提取关键词作为utm_term
def add_utm_with_term_from_query(from_url, to_url, term_param="q"):
    """
    从来源链接的查询参数中提取关键词作为utm_term（如搜索词）
    
    参数:
        from_url (str): 来源链接（可能包含查询参数，如 "https://xxx.com/search?q=python"）
        to_url (str): 目标链接
        term_param (str): 来源链接中存储关键词的参数名（默认"q"）
    
    返回:
        str: 包含utm_term的目标链接（若来源无关键词则不添加）
    """
    # 提取utm_source（复用逻辑）
    parsed_from = urlparse(from_url)
    domain_parts = parsed_from.netloc.split('.')
    source_parts = domain_parts[:-1] if len(domain_parts) > 1 else domain_parts
    utm_source = '_'.join(source_parts)
    
    # 提取来源链接中的关键词作为utm_term
    from_query = parse_qs(parsed_from.query)
    utm_term = from_query.get(term_param, [None])[0]  # 取第一个值
    
    # 固定基础参数
    utm_medium = "discover_page"
    utm_campaign = "content_cta"
    
    # 处理目标链接
    parsed_to = urlparse(to_url)
    query_params = parse_qs(parsed_to.query)
    query_params['utm_source'] = [utm_source]
    query_params['utm_medium'] = [utm_medium]
    query_params['utm_campaign'] = [utm_campaign]
    
    # 若有关键词则添加utm_term
    if utm_term:
        query_params['utm_term'] = [utm_term]
    
    new_query = urlencode(query_params, doseq=True)
    return urlunparse(parsed_to._replace(query=new_query))


# 补充函数4：保留目标链接已有的UTM参数（不覆盖）
def add_utm_preserve_existing(from_url, to_url):
    """
    仅为目标链接添加缺失的UTM参数，保留已有的参数值
    
    参数:
        from_url (str): 来源链接
        to_url (str): 目标链接（可能已包含部分UTM参数）
    
    返回:
        str: 补充UTM参数后的目标链接（不覆盖已有）
    """
    # 提取utm_source
    parsed_from = urlparse(from_url)
    domain_parts = parsed_from.netloc.split('.')
    source_parts = domain_parts[:-1] if len(domain_parts) > 1 else domain_parts
    utm_source = '_'.join(source_parts)
    
    # 基础参数
    utm_medium = "discover_page"
    utm_campaign = "content_cta"
    
    # 处理目标链接（仅添加缺失参数）
    parsed_to = urlparse(to_url)
    query_params = parse_qs(parsed_to.query)
    
    # 仅在参数不存在时添加
    if 'utm_source' not in query_params:
        query_params['utm_source'] = [utm_source]
    if 'utm_medium' not in query_params:
        query_params['utm_medium'] = [utm_medium]
    if 'utm_campaign' not in query_params:
        query_params['utm_campaign'] = [utm_campaign]
    
    new_query = urlencode(query_params, doseq=True)
    return urlunparse(parsed_to._replace(query=new_query))


# 测试案例
if __name__ == "__main__":
    print("=== 原有函数测试 ===")
    from_url1 = "https://github.com/XiaomingX/utm-generator-dev"
    to_url1 = "https://jobleap.cn/"
    print(add_utm_params(from_url1, to_url1))  # utm_source=github_XiaomingX
    
    print("\n=== 补充函数1：自定义medium和campaign ===")
    print(add_custom_utm_params(
        from_url="https://blog.jobleap4u.com",
        to_url="https://jobleap.cn/career",
        utm_medium="blog_post",
        utm_campaign="career_guide"
    ))  # 包含 utm_medium=blog_post
    
    print("\n=== 补充函数2：处理无协议的来源链接 ===")
    print(add_utm_from_incomplete_url(
        from_url="mp.jobleap4u.com",  # 无http/https
        to_url="https://jobleap.cn/jobs"
    ))  # 正确提取 utm_source=mp_jobleap4u
    
    print("\n=== 补充函数3：提取关键词作为utm_term ===")
    print(add_utm_with_term_from_query(
        from_url="https://search.jobleap4u.com?keyword=数据分析师",  # 包含关键词参数
        to_url="https://jobleap.cn/search",
        term_param="keyword"  # 指定关键词参数名为keyword
    ))  # 包含 utm_term=数据分析师
    
    print("\n=== 补充函数4：保留目标链接已有UTM参数 ===")
    print(add_utm_preserve_existing(
        from_url="https://wechat.jobleap4u.com",
        to_url="https://jobleap.cn?utm_source=wechat_old&utm_medium=old"  # 已有部分参数
    ))  # 保留原有utm_source，仅添加utm_campaign
