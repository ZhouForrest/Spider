import uuid
import traceback

from scrapy.selector import Selector

from hive_worker_hot_coffee.parsers.manual_parser import ManualBaseParser
from .field_mapping import map_field, replace_space
from hive_framework_milk.commons.utils.selector_util import clean_html


class Parser__qyxg_xzxk__credit_tonghua(ManualBaseParser):
    """
    class Parser__qyxg_xzxk__credit_tonghaufor
    行政许可-信用中国（通化）解析
    """

    name = "Parser__qyxg_xzxk__credit_tonghua"
    parser_info = "行政许可-信用中国（通化）解析"
    base_dict = {
        "version": 1,
    }

    def parse(self, source, *args, **kwargs):
        """
        parse logic
        :Keyword Arguments:
         self     --
         source   --
         *args    --
         **kwargs --
        :return: None
        """
        try:
            detail_html = clean_html(source.pop('bbd_html', ''))
            detail_url = source.get('bbd_url', '')
            self.logger.info('开始解析:{} {}'.format(self.parser_info, detail_url))
            response = Selector(text=detail_html)
            msg = response.xpath('//*[@id="company-messages-tab"]/div/div/div/div')
            res_list = []
            for j in range(1, int(len(msg) - 1), 2):
                res_dict = {}
                info = msg[j].xpath('./ul/li/p/text()').extract()
                for i in range(0, int(len(info) - 1), 2):
                    res_dict[replace_space(info[i])] = replace_space(info[i + 1])
                res_dict["_id"] = "{}".format(uuid.uuid4())
                res_dict["bbd_html"] = ""
                res_dict = map_field(res_dict)
                res_list.append(res_dict)
            return res_list
        except Exception as err:
            msg = '{} parse error! msg:{}'.format(self.parser_info, traceback.format_exc())
            self.logger.warning(msg)
