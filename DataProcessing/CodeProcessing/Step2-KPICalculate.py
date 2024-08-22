import pandas as pd
import os

for file in os.listdir("../0-Logsummary"):
    store_id = int(file.split('.')[0])
    researchdata = pd.read_csv('../0-Logsummary/' + file)
    researchdata = researchdata.iloc[1:]
    researchdata['DelegationDecision_demand'] = (researchdata['week_order_category'] - researchdata['modif_category_count']) / \
                                  researchdata['week_order_category']
    researchdata['DelegationDecision'] = (researchdata['week_order_item'] - researchdata['modif_count']) / researchdata[
        'week_order_item']

    researchdata['DelegationDecision_bakery'] = (researchdata['week_order_bakery_item'] - researchdata['modif_bakery_count']) / \
                                       researchdata['week_order_bakery_item']
    researchdata['DelegationDecision_dairy'] = (researchdata['week_order_dairy_item'] - researchdata['modif_dairy_count']) / \
                                      researchdata['week_order_dairy_item']
    researchdata['DelegationDecision_price10'] = (researchdata['week_order_price10_item'] - researchdata[
        'modif_price10_count']) / researchdata['week_order_price10_item']
    researchdata['DelegationDecision_price20'] = (researchdata['week_order_price20_item'] + researchdata[
        'week_order_price20above_item'] - researchdata['modif_price20_count'] - researchdata[
                                             'modif_price20above_count']) / (
                                                    researchdata['week_order_price20_item'] + researchdata[
                                                'week_order_price20above_item'])

    researchdata['sale_improvement'] = (researchdata['week_sale_value'] - researchdata['pre_sale']) / researchdata[
        'pre_sale']
    researchdata['sale_bakery_improvement'] = (researchdata['week_bakery_sale_value'] - researchdata[
        'pre_sale_bakery']) / researchdata['pre_sale_bakery']
    researchdata['sale_dairy_improvement'] = (researchdata['week_dairy_sale_value'] - researchdata['pre_sale_dairy']) / \
                                             researchdata['pre_sale_dairy']
    researchdata['sale_price10_improvement'] = (researchdata['week_price10_sale_value'] - researchdata[
        'pre_sale_price10']) / researchdata['pre_sale_bakery']
    researchdata['sale_price20_improvement'] = (researchdata['week_price20_sale_value'] + researchdata[
        'week_price20above_sale_value'] - researchdata['pre_sale_price20'] - researchdata['pre_sale_price20above']) / (
                                                           researchdata['pre_sale_price20'] + researchdata[
                                                       'pre_sale_price20above'])

    researchdata['Manager_outperform'] = (researchdata['week_AI_Shortage'] + researchdata['week_AI_Perish'] -
                                          researchdata['week_manager_Shortage'] - researchdata['week_manager_Perish']) / \
                                         researchdata['week_sale_value']
    researchdata['Manager_outperform_bakery'] = (researchdata['week_AI_bakery_Shortage'] + researchdata[
        'week_AI_bakery_Perish'] - researchdata['week_manager_bakery_Shortage'] - researchdata[
                                                     'week_manager_bakery_Perish']) / researchdata[
                                                    'week_bakery_sale_value']
    researchdata['Manager_outperform_dairy'] = (researchdata['week_AI_dairy_Shortage'] + researchdata[
        'week_AI_dairy_Perish'] - researchdata['week_manager_dairy_Shortage'] - researchdata[
                                                    'week_manager_dairy_Perish']) / researchdata[
                                                   'week_dairy_sale_value']
    researchdata['Manager_outperform_price10'] = (researchdata['week_AI_price10_Shortage'] + researchdata[
        'week_AI_price10_Perish'] - researchdata['week_manager_price10_Shortage'] - researchdata[
                                                      'week_manager_price10_Perish']) / researchdata[
                                                     'week_price10_sale_value']
    researchdata['Manager_outperform_price20'] = (researchdata['week_AI_price20_Shortage'] + researchdata[
        'week_AI_price20_Perish'] - researchdata['week_manager_price20_Shortage'] - researchdata[
                                                      'week_manager_price20_Perish']) / researchdata[
                                                     'week_price20_sale_value']

    target_feature = ['date', 'DelegationDecision_demand', 'DelegationDecision', 'DelegationDecision_bakery', 'DelegationDecision_dairy', 'DelegationDecision_price10',
                      'DelegationDecision_price20', 'sale_improvement', 'sale_bakery_improvement', 'sale_dairy_improvement',
                      'sale_price10_improvement', 'sale_price20_improvement', 'Manager_outperform',
                      'Manager_outperform_bakery', 'Manager_outperform_dairy', 'Manager_outperform_price10',
                      'Manager_outperform_price20']
    researchdata_reduced = researchdata[target_feature]

    researchdata_reduced.to_csv('../1-KPIsummary/' + str(store_id) + '.csv', index=False)