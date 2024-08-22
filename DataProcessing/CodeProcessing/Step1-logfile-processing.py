import pandas as pd
import numpy as np
import os


def Load_factors(Modification_list, Inventory_list, replenishment, current_date):
    #load pre-period performance by category
    my_add = 0

    pre_evaluation_date = current_date + pd.DateOffset(-30)  # use previous 30 days as store performance evaluation.

    pre_inventory = Inventory_list.loc[(Inventory_list.date >= pre_evaluation_date)
                                       & (Inventory_list.date < current_date)].copy()
    pre_calculation = pd.merge(pre_inventory, Price_list, on='product_id',how='left')
    pre_calculation = pd.merge(pre_calculation,productcategory, on='product_id',how='left')
    shortage_calculation = pre_calculation.loc[pre_calculation.inventory_end_of_day == 0].copy()
    shortage_calculation['missing_hour'] = [24 - row.hour if row.hour >= 6 else 18 for row in
                                            shortage_calculation.last_selling_time.tolist()]


    ###calculate sale, perish, shortage performance before system deployment
    pre_sale = np.sum(pre_calculation['sale'] * pre_calculation['selling_price']) / 30 * 7
    pre_perish = np.sum(pre_calculation['inventory_perish'] * pre_calculation['purchase_price']) / 30 * 7
    pre_shortage = np.sum(
        shortage_calculation.sale / (24 - shortage_calculation.missing_hour) * shortage_calculation.missing_hour *
        shortage_calculation.selling_price) / 30 * 7

    output_index = 0
    current_week = current_date.week
    start_date = current_date


    pre_calculation_dairy=pre_calculation.loc[pre_calculation.big_class=='牛奶']
    pre_calculation_bakery=pre_calculation.loc[pre_calculation.big_class=='烘焙']
    pre_calculation_price10=pre_calculation.loc[pre_calculation.selling_price<=10]
    pre_calculation_price20=pre_calculation.loc[(pre_calculation.selling_price<20)&(pre_calculation.selling_price>10)]
    pre_calculation_price20above=pre_calculation.loc[pre_calculation.selling_price>=20]

    pre_sale_dairy = np.sum(pre_calculation_dairy['sale'] * pre_calculation_dairy['selling_price']) / 30 * 7
    pre_sale_bakery = np.sum(pre_calculation_bakery['sale'] * pre_calculation_bakery['selling_price']) / 30 * 7

    pre_sale_price10 = np.sum(pre_calculation_price10['sale'] * pre_calculation_price10['selling_price']) / 30 * 7
    pre_sale_price20 = np.sum(pre_calculation_price20['sale'] * pre_calculation_price20['selling_price']) / 30 * 7
    pre_sale_price20above = np.sum(pre_calculation_price20above['sale'] * pre_calculation_price20above['selling_price']) / 30 * 7


    #count delegation decisions.
    result_list = []

    dele_category_count=0

    modif_count=0
    modif_dairy_count=0
    modif_bakery_count=0
    modif_price10_count=0
    modif_price20_count=0
    modif_price20above_count=0

    modif_category_count=0
    modif_dairy_category_count=0
    modif_bakery_category_count=0
    modif_price10_category_count=0
    modif_price20_category_count=0
    modif_price20above_category_count=0

    for i in range(Modification_list.shape[0]):
        this_record = Modification_list.loc[i]
        this_product = this_record.product_id
        if this_product not in productcategory['product_id'].values:
            print(this_product,this_record.product_name)
        else:
            this_purchase_price = Price_list.loc[Price_list['product_id'] == this_product]['purchase_price'].values[0]
            this_sell_price = Price_list.loc[Price_list['product_id'] == this_product]['selling_price'].values[0]

            manag_order = this_record.expect_bymanager
            model_order = this_record.forecast
            change_cate=np.abs(manag_order-model_order)
            # reason = str(this_record.reason)

            this_week = this_record.order_date.week

            if this_week == current_week:
                dele_category_count+=model_order
                modif_count+=1
                modif_category_count+=change_cate

                if productcategory.loc[productcategory.product_id==this_product,'big_class'].values[0]=='烘焙':
                    modif_bakery_count+=1
                    modif_bakery_category_count+=change_cate
                if productcategory.loc[productcategory.product_id==this_product,'big_class'].values[0]=='牛奶':
                    modif_dairy_count+=1
                    modif_dairy_category_count+=change_cate
                if this_sell_price<10:
                    modif_price10_count+=1
                    modif_price10_category_count+=change_cate
                elif this_sell_price<20:
                    modif_price20_count+=1
                    modif_price20_category_count+=change_cate
                else:
                    modif_price20above_count+=1
                    modif_price20above_category_count+=change_cate

            else:
                result_list.append([current_date] + [dele_category_count,modif_count,modif_category_count,modif_bakery_count,modif_bakery_category_count,modif_dairy_count,modif_dairy_category_count,modif_price10_count,modif_price10_category_count,modif_price20_count,modif_price20_category_count,modif_price20above_count,modif_price20above_category_count])

                if this_record.order_date.year == 2019 and my_add == 0:
                    my_add = current_week
                current_week = this_week
                current_date = this_record.order_date

                dele_category_count=0

                modif_count=0
                modif_dairy_count=0
                modif_bakery_count=0
                modif_price10_count=0
                modif_price20_count=0
                modif_price20above_count=0

                modif_category_count=0
                modif_dairy_category_count=0
                modif_bakery_category_count=0
                modif_price10_category_count=0
                modif_price20_category_count=0
                modif_price20above_category_count=0

                dele_category_count+=model_order
                modif_count+=1
                modif_category_count+=change_cate

                if productcategory.loc[productcategory.product_id==this_product,'big_class'].values[0]=='烘焙':
                    modif_bakery_count+=1
                    modif_bakery_category_count+=change_cate
                if productcategory.loc[productcategory.product_id==this_product,'big_class'].values[0]=='牛奶':
                    modif_dairy_count+=1
                    modif_dairy_category_count+=change_cate
                if this_sell_price<=10:
                    modif_price10_count+=1
                    modif_price10_category_count+=change_cate
                elif this_sell_price<=20:
                    modif_price20_count+=1
                    modif_price20_category_count+=change_cate
                else:
                    modif_price20above_count+=1
                    modif_price20above_category_count+=change_cate

    weekly_delegation=pd.DataFrame(result_list, columns=['date','dele_category_count','modif_count','modif_category_count','modif_bakery_count','modif_bakery_category_count','modif_dairy_count','modif_dairy_category_count','modif_price10_count','modif_price10_category_count','modif_price20_count','modif_price20_category_count','modif_price20above_count','modif_price20above_category_count'])


    current_date = start_date

    week_sale_value = 0
    week_perish = 0
    week_shortage = 0

    week_dairy_sale_value = 0
    week_dairy_perish = 0
    week_dairy_shortage = 0

    week_bakery_sale_value = 0
    week_bakery_perish = 0
    week_bakery_shortage = 0

    week_price10_sale_value = 0
    week_price10_perish = 0
    week_price10_shortage = 0

    week_price20_sale_value = 0
    week_price20_perish = 0
    week_price20_shortage = 0

    week_price20above_sale_value = 0
    week_price20above_perish = 0
    week_price20above_shortage = 0

    current_week = current_date.week

    post_inventory = Inventory_list.loc[(Inventory_list.date >= current_date)].copy()
    post_inventory = post_inventory.sort_values(by=['date']).reset_index(drop=True)

    result_total = []

    unsensored_demand={}
    for i in range(post_inventory.shape[0]):
        this_record = post_inventory.loc[i]
        this_product = this_record.product_id
        this_sale = this_record.sale
        this_perish = this_record.inventory_perish
        this_inventory = this_record.inventory_end_of_day
        this_purchase_price = Price_list.loc[Price_list['product_id'] == this_product]['purchase_price'].values[0]
        this_sell_price = Price_list.loc[Price_list['product_id'] == this_product]['selling_price'].values[0]

        if len(productcategory.loc[productcategory.product_id==this_product,'big_class'])==0:
            print(this_product,this_record.product_name)
        else:
            this_product_type=productcategory.loc[productcategory.product_id==this_product,'big_class'].values[0]

            if this_inventory == 0:
                if this_record.last_selling_time.hour >= 6:
                    this_shortage_hours = (24 - this_record.last_selling_time.hour)
                else:
                    this_shortage_hours = 18
                this_shortage_num=this_sale / (24 - this_shortage_hours) * this_shortage_hours
                this_shortage_value = this_shortage_num * this_sell_price
            else:
                this_shortage_num=0
                this_shortage_value = 0

            this_perish_value = this_perish * this_purchase_price
            this_sale_value = this_sale * this_sell_price
            this_week = this_record.date.week
            this_day=this_record.date.date()

            unsensored_demand[this_day,this_product]=this_sale+this_shortage_num

            if this_week == current_week:
                week_sale_value += this_sale_value
                week_perish += this_perish_value
                week_shortage += this_shortage_value

                if this_product_type=='烘焙':
                    week_bakery_sale_value += this_sale_value
                    week_bakery_perish += this_perish_value
                    week_bakery_shortage += this_shortage_value
                elif this_product_type=='牛奶':
                    week_dairy_sale_value += this_sale_value
                    week_dairy_perish += this_perish_value
                    week_dairy_shortage += this_shortage_value

                if this_sell_price<=10:
                    week_price10_sale_value += this_sale_value
                    week_price10_perish += this_perish_value
                    week_price10_shortage += this_shortage_value
                elif this_sell_price<=20:
                    week_price20_sale_value += this_sale_value
                    week_price20_perish += this_perish_value
                    week_price20_shortage += this_shortage_value
                else:
                    week_price20above_sale_value += this_sale_value
                    week_price20above_perish += this_perish_value
                    week_price20above_shortage += this_shortage_value
            else:
                result_total.append(
                    [current_date, week_sale_value, week_perish, week_shortage,
                     week_dairy_sale_value, week_dairy_perish, week_dairy_shortage,
                     week_bakery_sale_value, week_bakery_perish, week_bakery_shortage,
                     week_price10_sale_value, week_price10_perish, week_price10_shortage,
                     week_price20_sale_value, week_price20_perish, week_price20_shortage,
                     week_price20above_sale_value, week_price20above_perish, week_price20above_shortage,
                     pre_sale, pre_perish, pre_shortage,
                     pre_sale_dairy, pre_sale_bakery, pre_sale_price10, pre_sale_price20, pre_sale_price20above,
                     (current_date - start_date).days, int(week_sale_value / 10000)])
                if this_record.date.year == 2019 and my_add == 0:
                    my_add = current_week
                current_week = this_week
                current_date = this_record.date
                week_sale_value = 0
                week_perish = 0
                week_shortage = 0

                week_dairy_sale_value = 0
                week_dairy_perish = 0
                week_dairy_shortage = 0

                week_bakery_sale_value = 0
                week_bakery_perish = 0
                week_bakery_shortage = 0

                week_price10_sale_value = 0
                week_price10_perish = 0
                week_price10_shortage = 0

                week_price20_sale_value = 0
                week_price20_perish = 0
                week_price20_shortage = 0

                week_price20above_sale_value = 0
                week_price20above_perish = 0
                week_price20above_shortage = 0

                week_sale_value += this_sale_value
                week_perish += this_perish_value
                week_shortage += this_shortage_value

                if this_product_type=='烘焙':
                    week_bakery_sale_value += this_sale_value
                    week_bakery_perish += this_perish_value
                    week_bakery_shortage += this_shortage_value
                elif this_product_type=='牛奶':
                    week_dairy_sale_value += this_sale_value
                    week_dairy_perish += this_perish_value
                    week_dairy_shortage += this_shortage_value

                if this_sell_price<=10:
                    week_price10_sale_value += this_sale_value
                    week_price10_perish += this_perish_value
                    week_price10_shortage += this_shortage_value
                elif this_sell_price<=20:
                    week_price20_sale_value += this_sale_value
                    week_price20_perish += this_perish_value
                    week_price20_shortage += this_shortage_value
                else:
                    week_price20above_sale_value += this_sale_value
                    week_price20above_perish += this_perish_value
                    week_price20above_shortage += this_shortage_value

    weekly_sale=pd.DataFrame(result_total, columns=['date','week_sale_value','week_perish','week_shortage',
                     'week_dairy_sale_value','week_dairy_perish','week_dairy_shortage',
                     'week_bakery_sale_value','week_bakery_perish','week_bakery_shortage',
                     'week_price10_sale_value','week_price10_perish','week_price10_shortage',
                     'week_price20_sale_value','week_price20_perish','week_price20_shortage',
                     'week_price20above_sale_value','week_price20above_perish','week_price20above_shortage',
                     'pre_sale','pre_perish','pre_shortage', 'pre_sale_dairy','pre_sale_bakery','pre_sale_price10','pre_sale_price20','pre_sale_price20above',
                     'days','week_sale_value'])

    current_date = start_date
    week_order_category = 0 #total number of products
    week_order_value = 0 #total value of products
    week_order_item=0 #SKU nubmer

    week_order_dairy_category = 0
    week_order_dairy_value = 0
    week_order_dairy_item=0

    week_order_bakery_category = 0
    week_order_bakery_value = 0
    week_order_bakery_item=0

    week_order_price10_category = 0
    week_order_price10_value = 0
    week_order_price10_item=0

    week_order_price20_category = 0
    week_order_price20_value = 0
    week_order_price20_item=0

    week_order_price20above_category = 0
    week_order_price20above_value = 0
    week_order_price20above_item=0

    week_AI_Perish=0
    week_AI_Shortage=0
    week_manager_Perish=0
    week_manager_Shortage=0

    week_AI_dairy_Perish=0
    week_AI_dairy_Shortage=0
    week_manager_dairy_Perish=0
    week_manager_dairy_Shortage=0

    week_AI_bakery_Perish=0
    week_AI_bakery_Shortage=0
    week_manager_bakery_Perish=0
    week_manager_bakery_Shortage=0

    week_AI_price10_Perish=0
    week_AI_price10_Shortage=0
    week_manager_price10_Perish=0
    week_manager_price10_Shortage=0

    week_AI_price20_Perish=0
    week_AI_price20_Shortage=0
    week_manager_price20_Perish=0
    week_manager_price20_Shortage=0

    week_AI_price20above_Perish=0
    week_AI_price20above_Shortage=0
    week_manager_price20above_Perish=0
    week_manager_price20above_Shortage=0

    current_week = current_date.week

    result_total1 = []

    product_uncensored_demand=0

    for i in range(replenishment.shape[0]):
        this_record = replenishment.loc[i]
        this_product = this_record.product_id
        this_purchase_price = Price_list.loc[Price_list['product_id'] == this_product]['purchase_price'].values[0]
        this_sell_price = Price_list.loc[Price_list['product_id'] == this_product]['selling_price'].values[0]

        this_order_category = this_record.final_purchase_bymanager
        this_order_value = this_order_category * this_purchase_price

        this_order_AI=this_record.optimal_purchase_bymodel
        this_order_AI_value=this_order_AI * this_purchase_price
        demand_date = (this_record.order_date + pd.DateOffset(days=3)).date()

        (this_AI_Perish, this_AI_Shortage, this_manager_Perish, this_manager_Shortage) = (0, 0, 0, 0)
        if this_order_category!=this_order_AI:
            if (demand_date,this_product) in unsensored_demand.keys():
                product_uncensored_demand=unsensored_demand[demand_date,this_product]
            else:
                product_uncensored_demand=this_record.demand_third_day
            if this_order_category>product_uncensored_demand:
                this_manager_Perish=(this_order_category-product_uncensored_demand)*this_purchase_price
                this_manager_Shortage=0
            else:
                this_manager_Shortage=(product_uncensored_demand-this_order_category)*this_sell_price
                this_manager_Perish=0

            if this_order_AI>product_uncensored_demand:
                this_AI_Perish=(this_order_AI-product_uncensored_demand)*this_purchase_price
                this_AI_Shortage=0
            else:
                this_AI_Shortage=(product_uncensored_demand-this_order_AI)*this_sell_price
                this_AI_Perish=0


        this_product_type=productcategory.loc[productcategory.product_id==this_product,'big_class'].values[0]

        this_week = this_record.order_date.week


        if this_week == current_week:
            week_order_value += this_order_value
            week_order_category += this_order_category
            week_order_item+=1

            week_AI_Perish+=this_AI_Perish
            week_AI_Shortage+=this_AI_Shortage
            week_manager_Perish+=this_manager_Perish
            week_manager_Shortage+=this_manager_Shortage

            if this_product_type=='烘焙':
                week_order_bakery_category += this_order_category
                week_order_bakery_value += this_order_value
                week_order_bakery_item+=1
                week_AI_bakery_Perish+=this_AI_Perish
                week_AI_bakery_Shortage+=this_AI_Shortage
                week_manager_bakery_Perish+=this_manager_Perish
                week_manager_bakery_Shortage+=this_manager_Shortage

            elif this_product_type=='牛奶':
                week_order_dairy_category += this_order_category
                week_order_dairy_value += this_order_value
                week_order_dairy_item+=1
                week_AI_dairy_Perish+=this_AI_Perish
                week_AI_dairy_Shortage+=this_AI_Shortage
                week_manager_dairy_Perish+=this_manager_Perish
                week_manager_dairy_Shortage+=this_manager_Shortage

            if this_sell_price<=10:
                week_order_price10_category +=  this_order_category
                week_order_price10_value += this_order_value
                week_order_price10_item+=1
                week_AI_price10_Perish+=this_AI_Perish
                week_AI_price10_Shortage+=this_AI_Shortage
                week_manager_price10_Perish+=this_manager_Perish
                week_manager_price10_Shortage+=this_manager_Shortage

            elif this_sell_price<=20:
                week_order_price20_category += this_order_category
                week_order_price20_value += this_order_value
                week_order_price20_item+=1
                week_AI_price20_Perish+=this_AI_Perish
                week_AI_price20_Shortage+=this_AI_Shortage
                week_manager_price20_Perish+=this_manager_Perish
                week_manager_price20_Shortage+=this_manager_Shortage

            else:
                week_order_price20above_category += this_order_category
                week_order_price20above_value += this_order_value
                week_order_price20above_item+=1
                week_AI_price20above_Perish+=this_AI_Perish
                week_AI_price20above_Shortage+=this_AI_Shortage
                week_manager_price20above_Perish+=this_manager_Perish
                week_manager_price20above_Shortage+=this_manager_Shortage

        else:
            result_total1.append(
                [current_date, week_order_value, week_order_category, week_order_item,
                 week_order_bakery_value, week_order_bakery_category, week_order_bakery_item,
                 week_order_dairy_value, week_order_dairy_category, week_order_dairy_item,
                 week_order_price10_value, week_order_price10_category, week_order_price10_item,
                 week_order_price20_value, week_order_price20_category, week_order_price20_item,
                 week_order_price20above_value, week_order_price20above_category, week_order_price20above_item,
                 week_AI_Perish,week_AI_Shortage,week_manager_Perish,week_manager_Shortage,
                 week_AI_bakery_Perish,week_AI_bakery_Shortage,week_manager_bakery_Perish,week_manager_bakery_Shortage,
                 week_AI_dairy_Perish,week_AI_dairy_Shortage,week_manager_dairy_Perish,week_manager_dairy_Shortage,
                 week_AI_price10_Perish,week_AI_price10_Shortage,week_manager_price10_Perish,week_manager_price10_Shortage,
                 week_AI_price20_Perish,week_AI_price20_Shortage,week_manager_price20_Perish,week_manager_price20_Shortage,
                 week_AI_price20above_Perish,week_AI_price20above_Shortage,week_manager_price20above_Perish,week_manager_price20above_Shortage])
            if week_AI_Shortage=='':
                print('yes')
            if this_record.order_date.year == 2019 and my_add == 0:
                my_add = current_week
            current_week = this_week
            current_date = this_record.order_date

            week_order_category = 0 #total number of products
            week_order_value = 0 #total value of products
            week_order_item=0 #SKU nubmer

            week_order_dairy_category = 0
            week_order_dairy_value = 0
            week_order_dairy_item=0

            week_order_bakery_category = 0
            week_order_bakery_value = 0
            week_order_bakery_item=0

            week_order_price10_category = 0
            week_order_price10_value = 0
            week_order_price10_item=0

            week_order_price20_category = 0
            week_order_price20_value = 0
            week_order_price20_item=0

            week_order_price20above_category = 0
            week_order_price20above_value = 0
            week_order_price20above_item=0

            week_AI_Perish=0
            week_AI_Shortage=0
            week_manager_Perish=0
            week_manager_Shortage=0

            week_AI_dairy_Perish=0
            week_AI_dairy_Shortage=0
            week_manager_dairy_Perish=0
            week_manager_dairy_Shortage=0

            week_AI_bakery_Perish=0
            week_AI_bakery_Shortage=0
            week_manager_bakery_Perish=0
            week_manager_bakery_Shortage=0

            week_AI_price10_Perish=0
            week_AI_price10_Shortage=0
            week_manager_price10_Perish=0
            week_manager_price10_Shortage=0

            week_AI_price20_Perish=0
            week_AI_price20_Shortage=0
            week_manager_price20_Perish=0
            week_manager_price20_Shortage=0

            week_AI_price20above_Perish=0
            week_AI_price20above_Shortage=0
            week_manager_price20above_Perish=0
            week_manager_price20above_Shortage=0

            week_order_value += this_order_value
            week_order_category += this_order_category
            week_order_item+=1

            week_AI_Perish+=this_AI_Perish
            week_AI_Shortage+=this_AI_Shortage
            week_manager_Perish+=this_manager_Perish
            week_manager_Shortage+=this_manager_Shortage

            if this_product_type=='烘焙':
                week_order_bakery_category += this_order_category
                week_order_bakery_value += this_order_value
                week_order_bakery_item+=1
                week_AI_bakery_Perish+=this_AI_Perish
                week_AI_bakery_Shortage+=this_AI_Shortage
                week_manager_bakery_Perish+=this_manager_Perish
                week_manager_bakery_Shortage+=this_manager_Shortage

            elif this_product_type=='牛奶':
                week_order_dairy_category += this_order_category
                week_order_dairy_value += this_order_value
                week_order_dairy_item+=1
                week_AI_dairy_Perish+=this_AI_Perish
                week_AI_dairy_Shortage+=this_AI_Shortage
                week_manager_dairy_Perish+=this_manager_Perish
                week_manager_dairy_Shortage+=this_manager_Shortage

            if this_sell_price<=10:
                week_order_price10_category +=  this_order_category
                week_order_price10_value += this_order_value
                week_order_price10_item+=1
                week_AI_price10_Perish+=this_AI_Perish
                week_AI_price10_Shortage+=this_AI_Shortage
                week_manager_price10_Perish+=this_manager_Perish
                week_manager_price10_Shortage+=this_manager_Shortage

            elif this_sell_price<=20:
                week_order_price20_category += this_order_category
                week_order_price20_value += this_order_value
                week_order_price20_item+=1
                week_AI_price20_Perish+=this_AI_Perish
                week_AI_price20_Shortage+=this_AI_Shortage
                week_manager_price20_Perish+=this_manager_Perish
                week_manager_price20_Shortage+=this_manager_Shortage

            else:
                week_order_price20above_category += this_order_category
                week_order_price20above_value += this_order_value
                week_order_price20above_item+=1
                week_AI_price20above_Perish+=this_AI_Perish
                week_AI_price20above_Shortage+=this_AI_Shortage
                week_manager_price20above_Perish+=this_manager_Perish
                week_manager_price20above_Shortage+=this_manager_Shortage

    weekly_sale_loss=pd.DataFrame(result_total1, columns=['date','week_order_value','week_order_category','week_order_item',
             'week_order_bakery_value','week_order_bakery_category','week_order_bakery_item',
             'week_order_dairy_value','week_order_dairy_category','week_order_dairy_item',
             'week_order_price10_value','week_order_price10_category','week_order_price10_item',
             'week_order_price20_value','week_order_price20_category','week_order_price20_item',
             'week_order_price20above_value','week_order_price20above_category','week_order_price20above_item',
             'week_AI_Perish','week_AI_Shortage','week_manager_Perish','week_manager_Shortage',
             'week_AI_bakery_Perish','week_AI_bakery_Shortage','week_manager_bakery_Perish','week_manager_bakery_Shortage',
             'week_AI_dairy_Perish','week_AI_dairy_Shortage','week_manager_dairy_Perish','week_manager_dairy_Shortage',
             'week_AI_price10_Perish','week_AI_price10_Shortage','week_manager_price10_Perish','week_manager_price10_Shortage',
             'week_AI_price20_Perish','week_AI_price20_Shortage','week_manager_price20_Perish','week_manager_price20_Shortage',
             'week_AI_price20above_Perish','week_AI_price20above_Shortage','week_manager_price20above_Perish','week_manager_price20above_Shortage'])

    weekly_summary = pd.merge(weekly_delegation, weekly_sale, on='date')
    weekly_summary = pd.merge(weekly_summary, weekly_sale_loss, on='date')

    return weekly_summary

Price_list=pd.read_excel(r'../OtherInputs/Product_Price.xlsx')
Price_list.fillna(0, inplace=True)
Price_list.drop('product_name',axis=1)
startlist=pd.read_csv(r'../OtherInputs/startlist.csv') # load model_start_list
file_list=os.listdir('../../RawData/')
file_list.sort()
productcategory=pd.read_excel(pd.ExcelFile('../OtherInputs/Product_category.xlsx'))

for file in file_list:
    if ".xlsx" in file:
        store_id=int(file.split('_')[1].split('.')[0])
        print(store_id)
        store_model_start=startlist.loc[startlist['store_id']==store_id].model_suggest_date

        xls = pd.ExcelFile('../../RawData/replenishment_'+str(store_id)+'.xlsx')
        Modification_list = pd.read_excel(xls, 'modify_delivery_by_manager')
        Inventory_list = pd.read_excel(xls, 'transcation_inventory')
        replenishment = pd.read_excel(xls, 'replenishment')

        Inventory_list.fillna(0, inplace=True)
        Inventory_list=Inventory_list.sort_values(by=['date']).reset_index(drop=True)

        replenishment.fillna(0, inplace=True)
        replenishment=replenishment.sort_values(by=['order_date']).reset_index(drop=True)

        current_date=Modification_list.loc[0].order_date

        weekly_summary_table=Load_factors(Modification_list,Inventory_list,replenishment,current_date)

        weekly_summary_table.to_csv(r'../0-Logsummary/'+str(store_id)+'.csv', index = False)