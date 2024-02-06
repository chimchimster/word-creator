from typing import Any

from .base import BaseMetaModel
from modules.apps.localization import ReportLanguagePicker


class CategorySocialMediaModel(BaseMetaModel):
    # CategoryName

    COUNTER: str
    name: str
    type: int

    @property
    def counter(self):
        return self.COUNTER

    def translate_model_fields(self, lang: str) -> None:
        if translation := ReportLanguagePicker(lang)().get('categories_soc'):
            self.name = translation.get(self.name, '')


class CategoryMassMediaModel(BaseMetaModel):
    # CategoryName2

    COUNTER: str
    name_cat: str

    @property
    def counter(self):
        return self.COUNTER

    def translate_model_fields(self, lang: str) -> None:
        if translation := ReportLanguagePicker(lang)().get('categories_smi'):
            self.name_cat = translation.get(self.name_cat, '')


class ItemsCountMassMediaModel(BaseMetaModel):
    # ItemsCount

    COUNTER: str
    res_id: int
    RESOURCE_NAME: str

    @property
    def counter(self):
        return self.COUNTER


class ItemsCountSocialMediaModel(BaseMetaModel):
    # ItemsCount2
    COUNTER: str
    res_id: int
    resource_name: str

    @property
    def counter(self):
        return self.COUNTER


class ItemsMassMediaModel(BaseMetaModel):
    # f_news

    id: str
    title: str
    nd_date: int
    not_date: str
    content: str
    link: str
    news_link: str
    res_id: str
    RESOURCE_NAME: str
    RESOURCE_PAGE_URL: str
    sentiment: int
    full_text: str

    @property
    def resource_name(self):
        return self.RESOURCE_NAME

    @property
    def resource_page_url(self):
        return self.RESOURCE_PAGE_URL


class ItemsSocialMediaModel(BaseMetaModel):
    # f_news2

    id: str
    title: str
    date: int
    text: str
    link: str
    res_id: str
    type: int
    news_link: str
    resource_name: str
    res_link: str
    members: int
    sentiment: int
    full_text: str


class IMASResponseAPIModel(BaseMetaModel):
    analyzer_tags_changed: str
    categoryNames: list[CategoryMassMediaModel]
    categoryNames2: list[CategorySocialMediaModel]
    itemsCount: list[ItemsCountMassMediaModel]
    itemsCount2: list[ItemsCountSocialMediaModel]
    f_news: list[ItemsMassMediaModel]
    f_news2: list[ItemsSocialMediaModel]

    @property
    def tags(self):
        return self.analyzer_tags_changed

    @property
    def category_mass_media(self):
        return self.categoryNames

    @property
    def category_social_media(self):
        return self.categoryNames2

    @property
    def items_count_mass_media(self):
        return self.itemsCount

    @property
    def items_count_social_media(self):
        return self.itemsCount2

    @property
    def items_mass_media(self):
        return self.f_news

    @property
    def items_social_media(self):
        return self.f_news2


__all__ = [
    'IMASResponseAPIModel',
]