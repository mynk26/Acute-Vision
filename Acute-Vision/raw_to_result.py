raw = [{"model": "attendance.attendance", "pk": 1, "fields": {"Enrollment": 24, "Subject_Code": "1", "Section": "CSE-1A", "Date": "2020-11-16", "Status": "A"}}, {"model": "attendance.attendance", "pk": 2, "fields": {"Enrollment": 24, "Subject_Code": "2", "Section": "CSE-1A", "Date": "2020-11-16", "Status": "P"}}, {"model": "attendance.attendance", "pk": 3, "fields": {"Enrollment": 25, "Subject_Code": "1", "Section": "CSE-1A", "Date": "2020-11-16", "Status": "P"}}, {"model": "attendance.attendance", "pk": 4, "fields": {"Enrollment": 25, "Subject_Code": "2", "Section": "CSE-1A", "Date": "2020-11-16", "Status": "P"}}, {"model": "attendance.attendance", "pk": 6, "fields": {"Enrollment": 26, "Subject_Code": "1", "Section": "CSE-1A", "Date": "2020-11-16", "Status": "P"}}, {"model": "attendance.attendance", "pk": 7, "fields": {"Enrollment": 26, "Subject_Code": "2", "Section": "CSE-1A", "Date": "2020-11-16", "Status": "P"}}, {"model": "attendance.attendance", "pk": 8, "fields": {"Enrollment": 27, "Subject_Code": "1", "Section": "CSE-1A", "Date": "2020-11-16", "Status": "P"}}, {"model": "attendance.attendance", "pk": 9, "fields": {"Enrollment": 28, "Subject_Code": "1", "Section": "CSE-1A", "Date": "2020-11-16", "Status": "P"}}, {"model": "attendance.attendance", "pk": 10, "fields": {"Enrollment": 28, "Subject_Code": "2", "Section": "CSE-1A", "Date": "2020-11-16", "Status": "P"}}, {"model": "attendance.attendance", "pk": 11, "fields": {"Enrollment": 27, "Subject_Code": "2", "Section": "CSE-1A", "Date": "2020-11-16", "Status": "P"}}]

def raw_to_result(raw):
    result = {}
    total = 0
    for ele in raw:
        if ele['fields']['Subject_Code'] in result:
            if ele['fields']['Enrollment'] in result[ele['fields']['Subject_Code']]:
                if ele['fields']['Status']=='P':
                    result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['P']+=1
                    total += 1
                elif ele['fields']['Status']=='A':
                    result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['A']+=1
                    total += 1

            else:
                result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]={}
                if ele['fields']['Status']=='P':
                    total = 1
                    result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['P']=1
                    result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['A']=0
                elif ele['fields']['Status']=='A':
                    total = 1
                    result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['P']=0
                    result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['A']=1

        else:
            result[ele['fields']['Subject_Code']]={}
            result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]={}
            if ele['fields']['Status']=='P':
                total = 1
                result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['P']=1
                result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['A']=0
            elif ele['fields']['Status']=='A':
                total = 1
                result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['P']=0
                result[ele['fields']['Subject_Code']][ele['fields']['Enrollment']]['A']=1
    return (result,total)
    
print(raw_to_result(raw))