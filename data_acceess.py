from selenium import webdriver
from selenium.webdriver.support.ui import Select
import itertools
import time
from helper_functions import *
import os
import pandas as pd
import datetime


CHROMEDRIVER_PATH = os.path.join('~', 'chromedriver')  # or your own path

TARGET_FUND_SYM_LIST = ['LU1861219704:USD']


class FundWebAccessHelper:
    def __init__(self):
        self.driver = webdriver.Chrome(CHROMEDRIVER_PATH)
        self.result_dict = {}
        self.target_start_dict = {}
        self.target_end_dict = {}
        self.target_start_date = None
        self.target_end_date = None
        self.reset_target_start_end()

    def reset_target_start_end(self):
        today_date = datetime.datetime.today().date()
        self.target_start_date = str(datetime.datetime(today_date.year - 1, today_date.month, today_date.day).date())
        self.target_end_date = str(today_date)
        self.target_start_dict = {'year': today_date.year - 1, 'month': today_date.month, 'day': today_date.day}
        self.target_end_dict = {'year': today_date.year, 'month': today_date.month, 'day': today_date.day}
        return

    def set_target_start(self, input_start_date):
        self.target_start_date = input_start_date
        self.target_start_dict['year'] = int(input_start_date[:4])
        self.target_start_dict['month'] = int(input_start_date[5:7])
        self.target_start_dict['day'] = int(input_start_date[8:10])
        return

    def set_target_end(self, input_end_date):
        self.target_end_date = input_end_date
        self.target_end_dict['year'] = int(input_end_date[:4])
        self.target_end_dict['month'] = int(input_end_date[5:7])
        self.target_end_dict['day'] = int(input_end_date[8:10])
        pass

    def get_fund_target_start_end_data(self, input_fund_sym):
        print(f'Start getting {input_fund_sym} from {self.target_start_date} to {self.target_end_date}...')
        target_url = f'https://markets.ft.com/data/funds/tearsheet/historical?s={input_fund_sym}'
        self.driver.get(target_url)
        filter_button = a.driver.find_element_by_css_selector(
            'body > div.o-grid-container.mod-container > div:nth-child(2) > section.mod-main-content > div:nth-child(1)'
            ' > div > h2 > span')
        filter_button.click()
        time.sleep(0.3)

        # Target end date
        while 1:
            try:
                to_datepicker = self.driver.find_element_by_xpath(
                    '/html/body/div[3]/div[2]/section[3]/div[1]/div/div/div[1]/div[1]/div/form/fieldset/span/div[2]/'
                    'div[1]/input[1]')
                to_datepicker.click()
                break
            except:
                time.sleep(0.3)
                pass
        time.sleep(0.2)
        to_month_text = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[2]/section[3]/div[1]/div/div/div[1]/div[1]/div/form/fieldset/span/div[2]/'
            'div[2]/div/div/div/div/div/div/div[1]').text
        to_month_num = month_word_to_num(to_month_text)
        if to_month_num != self.target_end_dict['month']:
            while to_month_num != self.target_end_dict['month']:
                prev_button = a.driver.find_element_by_xpath(
                    '/html/body/div[3]/div[2]/section[3]/div[1]/div/div/div[1]/div[1]/div/form/fieldset/span/div[2]/'
                    'div[2]/div/div/div/div/div/div/div[2]')
                prev_button.click()
                time.sleep(0.1)
                to_month_text = self.driver.find_element_by_xpath(
                    '/html/body/div[3]/div[2]/section[3]/div[1]/div/div/div[1]/div[1]/div/form/fieldset/span/div[2]/'
                    'div[2]/div/div/div/div/div/div/div[1]').text
                to_month_num = month_word_to_num(to_month_text)
            to_year_picker = a.driver.find_element_by_xpath(
                '/html/body/div[3]/div[2]/section[3]/div[1]/div/div/div[1]/div[1]/div/form/fieldset/span/div[2]/'
                'div[2]/div/div/div/div/div/div/select')
            select = Select(to_year_picker)
            select.select_by_value(str(self.target_end_dict['year']))
        to_date_tb = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[2]/section[3]/div[1]/div/div/div[1]/div[1]/div/form/fieldset/span/div[2]/'
            'div[2]/div/div/div/div/div/table')
        to_date_rows = [row.find_elements_by_tag_name('td') for row in to_date_tb.find_elements_by_tag_name('tr')]
        to_date_rows[0] = [i for i in to_date_rows[0] if int(i.text) <= 10]
        to_date_days = list(itertools.chain.from_iterable(to_date_rows))
        to_date_day_element = [i for i in to_date_days if int(i.text) == self.target_end_dict['day']][0]
        to_date_day_element.click()

        # Target start date
        while 1:
            try:
                from_datepicker = self.driver.find_element_by_xpath(
                    '/html/body/div[3]/div[2]/section[3]/div[1]/div/div/div[1]/div[1]/div/form/fieldset/span/div[1]/'
                    'div[1]/input[1]')
                from_datepicker.click()
                break
            except:
                time.sleep(0.3)
                pass
        time.sleep(0.2)
        from_month_text = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[2]/section[3]/div[1]/div/div/div[1]/div[1]/div/form/fieldset/span/div[1]/'
            'div[2]/div/div/div/div/div/div/div[1]').text
        from_month_num = month_word_to_num(from_month_text)
        if from_month_num != self.target_start_dict['month']:
            while from_month_num != self.target_start_dict['month']:
                prev_button = a.driver.find_element_by_xpath(
                    '/html/body/div[3]/div[2]/section[3]/div[1]/div/div/div[1]/div[1]/div/form/fieldset/span/div[1]/'
                    'div[2]/div/div/div/div/div/div/div[2]')
                prev_button.click()
                time.sleep(0.1)
                from_month_text = self.driver.find_element_by_xpath(
                    '/html/body/div[3]/div[2]/section[3]/div[1]/div/div/div[1]/div[1]/div/form/fieldset/span/div[1]/'
                    'div[2]/div/div/div/div/div/div/div[1]').text
                from_month_num = month_word_to_num(from_month_text)
            from_year_picker = a.driver.find_element_by_xpath(
                '/html/body/div[3]/div[2]/section[3]/div[1]/div/div/div[1]/div[1]/div/form/fieldset/span/div[1]/'
                'div[2]/div/div/div/div/div/div/select')
            select = Select(from_year_picker)
            select.select_by_value(str(self.target_start_dict['year']))
        from_date_tb = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[2]/section[3]/div[1]/div/div/div[1]/div[1]/div/form/fieldset/span/div[1]/'
            'div[2]/div/div/div/div/div/table')
        from_date_rows = [row.find_elements_by_tag_name('td') for row in from_date_tb.find_elements_by_tag_name('tr')]
        from_date_rows[0] = [i for i in from_date_rows[0] if int(i.text) <= 10]
        from_date_days = list(itertools.chain.from_iterable(from_date_rows))
        from_date_day_element = [i for i in from_date_days if int(i.text) == self.target_start_dict['day']][0]
        from_date_day_element.click()

        # Get data
        print(f'[{input_fund_sym}] - Processing table ...')
        while 1:
            df = self.get_table_data()
            if df.loc[df['date_time'] < self.target_start_date, :].shape[0] == 0 and \
                    df.loc[df['date_time'] > self.target_end_date, :].shape[0] == 0:
                break
            else:
                print('Try again as wrong data of wrong dates are called')
        print(f'[{input_fund_sym}] - Done!')
        return df
    
    def get_table_data(self):
        while 1:
            try:
                target_tb = self.driver.find_element_by_css_selector(
                    'body > div.o-grid-container.mod-container > div:nth-child(2) > section.mod-main-content > '
                    'div:nth-child(1) > div > div > div.mod-ui-table--freeze-pane__container >'
                    ' div.mod-ui-table--freeze-pane__scroll-container > table')
                break
            except:
                time.sleep(0.3)
                pass
        
        while 1:
            try:
                rows = [row.find_elements_by_tag_name('td') for row in target_tb.find_elements_by_tag_name('tr')]
                rows = [row for row in rows if len(row)]
                parsed_data = [[i.text for i in row] for row in rows]
                break
            except:
                time.sleep(0.3)
                pass
        tmp_df = pd.DataFrame(parsed_data, columns=['date_time', 'open', 'high', 'low', 'close', 'volume'])
        tmp_df = tmp_df[['date_time', 'open', 'high', 'low', 'close']]
        tmp_df.loc[:, 'date_time'] = tmp_df['date_time'].apply(
            lambda x: datetime.datetime.strptime(x[x.find(' ') + 1:], '%B %d, %Y').strftime('%Y-%m-%d'))
        try:
            tmp_df.loc[:, ['open', 'high', 'low', 'close']] = tmp_df[['open', 'high', 'low', 'close']].astype(float)
        except:
            pass
        return tmp_df

    def get_one_fund_all_data(self, input_fund_sym, input_start_date, input_end_date):
        print(f'Getting {input_fund_sym} data from {input_start_date} to {input_end_date}')
        tmp_end = input_end_date
        tmp_start = str((datetime.datetime.strptime(tmp_end, '%Y-%m-%d') - datetime.timedelta(days=300)).date())
        res_df_list = []
        while tmp_start > input_start_date:
            self.set_target_start(tmp_start)
            self.set_target_end(tmp_end)
            print(f'{input_fund_sym} - Getting slice {tmp_start} to {tmp_end}')
            res_df_list.append(self.get_fund_target_start_end_data(input_fund_sym))
            tmp_end = tmp_start
            tmp_start = str((datetime.datetime.strptime(tmp_end, '%Y-%m-%d') - datetime.timedelta(days=300)).date())
        tmp_start = input_start_date
        self.set_target_start(tmp_start)
        self.set_target_end(tmp_end)
        print(f'{input_fund_sym} - Getting slice {tmp_start} to {tmp_end}')
        res_df_list.append(self.get_fund_target_start_end_data(input_fund_sym))
        res_df = pd.concat(res_df_list, join='outer').reset_index(drop=True)
        print(f'Finished getting {input_fund_sym} data from {input_start_date} to {input_end_date}')
        return res_df


def month_word_to_num(input_month_word):
    return int(datetime.datetime.strptime(input_month_word, '%B').strftime('%m'))


def month_num_to_word(input_month_num):
    return datetime.date(1900, input_month_num, 1).strftime('%B')


if __name__ == '__main__':

    # Construct helper instance
    a = FundWebAccessHelper()

    # Set start date and end date for config, and then call the data
    df = a.get_one_fund_all_data(input_fund_sym=TARGET_FUND_SYM_LIST[0],
                                 input_start_date='2019-01-01',
                                 input_end_date='2021-02-10')



