from cv2 import contourArea
from numpy import int0

def save_vector_get(list:list, x:int, y:int):
    try:
        return list[x][y]
    except:
        return None
    
def save_list_get(list:list, i:int):
    try:
        return list[i]
    except:
        return None

def dictKAHatributes(numList, cellsByRow) -> dict:
    """Записывает в словарь к каждому атрибуту соответствующую ячейку из распознанных (В соответствии с макетом таблицы)

    Args:
        numList [int]: Номер страницы
        cellsByRow [Array]: Массив из координат ячеек таблицы, разделённых по строкам

    Returns:
        dict: Словарь (Атрибут: Координаты соотв. ячейки)
    """
        
    coordinates = {}
    N_analysresult = 0
    N_Events = 0


    if numList == 1:
        c = cellsByRow
        # Проверки на существование элемента с координатами
        coordinates['modewritingmc'] =                  save_vector_get(c, 2, 1)
        coordinates['workcentermc'] =                   save_vector_get(c, 2, 2)
        coordinates['number'] =                         save_vector_get(c, 2, 3)
        coordinates['date'] =                           save_vector_get(c, 2, 4)
        coordinates['gdshl'] =                          save_vector_get(c, 5, 0)
        coordinates['gdsparentmc'] =                    save_vector_get(c, 5, 1)
        coordinates['factorynumber'] =                  save_vector_get(c, 5, 2)
        coordinates['productiondate'] =                 save_vector_get(c, 5, 3)
        coordinates['qty'] =                            save_vector_get(c, 5, 4)
        coordinates['qtydiscr'] =                       save_vector_get(c, 5, 5)
        coordinates['qtyreturn'] =                      save_vector_get(c, 5, 6)
        coordinates['detailkindmc'] =                   save_vector_get(c, 8, 4)
        coordinates['claimquerymc'] =                   save_vector_get(c, 8, 6)
        coordinates['objectiontoqualitykindmc'] =       save_vector_get(c, 8, 8)
        coordinates['dateincard'] =                     save_vector_get(c, 8, 9)
        coordinates['controlkindmc'] =                  save_vector_get(c, 8, 11)
        coordinates['outfactormc'] =                    save_vector_get(c, 8, 13)
        coordinates['dispforworkdetailmc'] =            save_vector_get(c, 8, -1)
        coordinates['disptypedescmc'] =                 save_vector_get(c, 9, -1)
        coordinates['disptypedeschl'] =                 save_vector_get(c, 9, 0)
        coordinates['disptypedeschl1'] =                save_vector_get(c, 10, 0)
        coordinates['disptypedeschl2'] =                save_vector_get(c, 11, 0)
        coordinates['disptypedeschl3'] =                save_vector_get(c, 12, 0)
        coordinates['creatorhl'] =                      save_vector_get(c, 12, -1)
        coordinates['disptypedescmc1'] =                save_vector_get(c, 17, -1)
        coordinates['faultcausemc'] =                   save_vector_get(c, 19, -1)
        coordinates['causezavodmc'] =                   save_vector_get(c, 21, 0)
        coordinates['causeworkcentermc'] =              save_vector_get(c, 23, 0)
        coordinates['causeuserhl'] =                    save_vector_get(c, 23, 1)
        coordinates['professionhl'] =                   save_vector_get(c, 23, 2)
        coordinates['causeworkcentermc2'] =             save_vector_get(c, 24, 0)
        coordinates['causeuserhl2'] =                   save_vector_get(c, 24, 1)
        coordinates['professionhl2'] =                  save_vector_get(c, 24, 2)
        coordinates['modewritingmc1'] =                 save_vector_get(c, 27, 0)
        coordinates['causeworkcentermc1'] =             save_vector_get(c, 27, 1)
        coordinates['conclofclaimmc'] =                 save_vector_get(c, 27, 5)
        coordinates['conclrepdispcntmc'] =              save_vector_get(c, 27, 7)
        coordinates['conclofreturnoutmc'] =             save_vector_get(c, 27, 9)
        coordinates['conclofusedetailmc'] =             save_vector_get(c, 27, 11)
        coordinates['resbacklogproductmc'] =            save_vector_get(c, 27, 13)
        coordinates['conclofrealdetailmc'] =            save_vector_get(c, 27, 15)
        coordinates['objectanalysmc'] =                 save_vector_get(c, 27, 17)

    if numList == 2:
        c = cellsByRow
        CellArea = 1
        idEventsCells = 0
        for i, row in enumerate(c):
            line = int0(row)
            areaRatio = abs(contourArea(line)/CellArea-1) # Соотношение площадей предыдущей ячейки с текущей
            if areaRatio < 0.3 and i != 0:
                coordinates[f'analysresult{i}'] = row[0]
            elif areaRatio > 0.3 and i != 0:
                idEventsCells = i + 2   # Идентификатор начала подтаблицы описания мероприятий устранения несоответствий
                                        #+2 для начала отсчёта от первой строки с полезной информацей
                N_analysresult = i                                            
                break
            CellArea = contourArea(line)
        
        c = c[idEventsCells:]
        for i, row in enumerate(c):
            if len(row) == 1:
                N_Events = i
                break
            if i == 0:
                continue
            coordinates[f'contentofevent{i}']   = save_list_get(row, 0)
            coordinates[f'duedate{i}']          = save_list_get(row, 1)
            coordinates[f'structurallink{i}']   = save_list_get(row, 2)
            coordinates[f'fio{i}']              = save_list_get(row, 3)
            coordinates[f'k{i}']                = save_list_get(row, 4)
            coordinates[f'completionmark{i}']   = save_list_get(row, 5)
    return coordinates, N_analysresult, N_Events
