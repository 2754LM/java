import json
import re
import pandas as pd
from pathlib import Path

# 这个函数纯AI写的
def clean_salary(salary):
    # 清洗薪资字段，统一转换为月薪(min_salary, max_salary)
    # 支持格式：100-500元/天、12-16K、20-30K·13薪、30-50K
    if not salary:
        return None, None
    # 处理日薪（如"100-500元/天"）
    daily_match = re.match(r'(\d+)-(\d+)元/天', salary)
    if daily_match:
        min_daily = int(daily_match.group(1))
        max_daily = int(daily_match.group(2))
        # 按每月22个工作日计算
        return min_daily * 22, max_daily * 22
    
    # 处理带薪数的（如"20-30K·13薪"）
    annual_match = re.match(r'(\d+)-(\d+)K·(\d+)薪', salary)
    if annual_match:
        min_monthly = int(annual_match.group(1)) * 1000
        max_monthly = int(annual_match.group(2)) * 1000
        months = int(annual_match.group(3))
        # 计算月薪（年薪/12）
        return int(min_monthly * months / 12), int(max_monthly * months / 12)
    
    # 处理普通月薪（如"12-16K"或"30-50K"）
    monthly_match = re.match(r'(\d+)-(\d+)K', salary)
    if monthly_match:
        return int(monthly_match.group(1)) * 1000, int(monthly_match.group(2)) * 1000
    return None, None
def clean_experience(experience):
    # 可能格式有 "1-3年"、"3-5年"、"5-10年"、"10年以上"、"经验不限"
    legal = ['1-3年', '3-5年', '5-10年', '10年以上', '经验不限']
    if experience in legal:
        return experience
    else:
        return '经验不限'
def clean_degree(degree):
    # 可能格式有 "本科"、"硕士"、"博士"、"大专"、"学历不限"
    legal = ['本科', '硕士', '博士', '大专', '学历不限']
    if degree in legal:
        return degree
    else:
        return '学历不限'
    
def is_legal(record):
    if(record['最低薪资'] is None or record['最高薪资'] is None ):
        return False
    if(record['最低薪资'] > record['最高薪资']):
        return False
    if 'java' not in record['岗位名称'].lower():
        return False
    return True
    
def clean_record(record):
    cleaned_record = {
        '岗位名称': record.get('jobName', 'N/A'),
        '最低薪资': record.get('salaryDesc', 'N/A'),
        '经验要求': record.get('jobExperience', 'N/A'),
        '学历要求': record.get('jobDegree', 'N/A'),
        '公司规模': record.get('brandScaleName', 'N/A'),
        '行业领域': record.get('brandIndustry', 'N/A'),
        '工作城市': record.get('cityName', 'N/A'),
        '技能要求': '、'.join(record.get('skills', []))
    }
    cleaned_record['最低薪资'],cleaned_record['最高薪资']  = clean_salary(cleaned_record['最低薪资'])
    cleaned_record['经验要求'] = clean_experience(cleaned_record['经验要求'])
    cleaned_record['学历要求'] = clean_degree(cleaned_record['学历要求'])
    if is_legal(cleaned_record):
        return cleaned_record
    else:
        return None
    
def process_boss_data(input_paths=['data/raw/raw_data_1.json', 'data/raw/raw_data_2.json'], 
                     output_path='data/processed/jobs_data.xlsx'):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    processed_data = []
    for input_path in input_paths:
        with open(input_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        for job in json_data:
            processed_job = clean_record(job)
            if processed_job is None:
                continue
            processed_data.append(processed_job)
            
    df = pd.DataFrame(processed_data)
    columns_order = [
        '岗位名称', '最低薪资','最高薪资', '经验要求', '学历要求',
        '技能要求', '工作城市','公司规模', '行业领域'
    ]
    df = df[columns_order]
    
    df.to_excel(output_path, index=False, engine='openpyxl')
    
    print(f"数据处理完成，结果已保存到: {Path(output_path).resolve()}")
    print(f"共处理 {len(df)} 条岗位数据")

