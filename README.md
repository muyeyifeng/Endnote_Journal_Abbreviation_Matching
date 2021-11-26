# Endnote_Journal_Abbreviation_Matching

The purpose of this project is not to perfect the journal name-abbreviation, but only to match the journal name and abbreviation of the reference in Endnote, so there is a phenomenon in the document that a journal has multiple names and corresponds to the same abbreviation.

本项目的目的并不是完善期刊名-缩写，仅仅是为了匹配Endnote中参考文献的期刊名及其缩写，所以文档中存在一种期刊拥有多个名称并对应同一缩写的现象。

How to use (Endnote x20):

    1.Export Journals List in Endnote (Library->Open Term Lists->Journals Term Lists->Lists->Export List...).

    2.Add the export Journals List file path in the bib_text[] list in the main() function.

    3.Run the main() function.

    4.The matching results are saved in Journal_abbreviation.txt,
    and the unmatched journals are saved in Unmatched_journals.yml.

    5.Unmatched journals need to be manually searched and added. The original intention of this project is to 
    satisfy its own use and will not actively improve the journal list (Journal_abbreviation.yml).

    6.Clear the default journal list in Endnote (Library->Open Term Lists->Journals Term Lists->Select All->Delete Term),
    and import The_result_of_this_run.txt (Library->Open Term Lists->Journals Term Lists->Lists ->Import List...)

使用方法（Endnote x20）：

    1.在Endnote中导出Journals List（Library->Open Term Lists->Journals Term Lists->Lists->Export List...）。
    
    2.在main()函数中的bib_text[]列表里添加导出Journals List文件路径。

    3.运行main()函数。

    4.匹配结果保存在The_result_of_this_run.txt，未匹配到的期刊保存在Unmatched_journals.yml。

    5.未匹配到的期刊需要手动查找添加，本项目的初衷是满足自身使用，并不会主动完善期刊列表（Journal_abbreviation.yml）。

    6.在Endnote中清空默认的期刊列表(Library->Open Term Lists->Journals Term Lists->选择所有->Delete Term）,
    并导入Journal_abbreviation.txt（Library->Open Term Lists->Journals Term Lists->Lists->Import List...）