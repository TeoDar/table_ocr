import json

def finalProcess(dictText, N_analysresult, N_Events):
    """Метод для финальной обработки полученного словаря и преобразования его в JSON

    Args:
        dictText (dict): Словарь полученный при распознавании текста
    """
    newDict = {}
    newDict = dictText.copy()
    newDict['analysresults'] = []
    for i in range(1, N_analysresult):
        newDict.pop(f'analysresult{i}') 
        newDict['analysresults'].append(dictText[f'analysresult{i}'])

    newDict['events'] = []
    for i in range(1, N_Events):
        newDict.pop(f'contentofevent{i}')
        newDict.pop(f'duedate{i}')
        newDict.pop(f'structurallink{i}')
        newDict.pop(f'fio{i}')
        newDict.pop(f'k{i}')
        newDict.pop(f'completionmark{i}')

        newDict['events'].append({
        f'contentofevent{i}':dictText[f'contentofevent{i}'],
        f'duedate{i}':dictText[f'duedate{i}'],
        f'structurallink{i}':dictText[f'structurallink{i}'],
        f'fio{i}':dictText[f'fio{i}'],
        f'k{i}':dictText[f'k{i}'],
        f'completionmark{i}':dictText[f'completionmark{i}']
        }
)

    
    JSON = json.dumps(newDict, ensure_ascii=False)
    return JSON
