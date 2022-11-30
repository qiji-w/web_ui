from selenium.webdriver.common.by import By

from page.op_base_page import OpBasePage


# 组件
class ElementDesign(OpBasePage):
    _click_date_design_locator = (By.CSS_SELECTOR,
                                  'span[data-testid="EventAnalysis_NewEventAnalysis_TimeRange_12"]'
                                  )

    # 调起时间组件
    def click_date_design(self):
        self.click(self._click_date_design_locator)
        return self

    pass
