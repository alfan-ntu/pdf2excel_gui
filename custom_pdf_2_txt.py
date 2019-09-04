import os
import constant
import class_set
import sys
import getopt
import pdb
import pdfminer
import pdfminer.high_level
import pdfminer.layout
import excel_output


def pdf_2_txt(input_file):
    print("pdf_2_txt receives a file named ", input_file)
    # input_file = ""                 # pdf input file
    textoutput_file = ""            # text output file
    output_file = ""                # output csv file

    tax_bill_list = []              # 稅單號碼
    declaration_form_list = []      # 報單號碼
    tax_ID_list = []                # 納稅義務人統一標號
    tax_amount_list = []            # 金額

    first_page = True               # end of Tax_ID of the 1st page differs from
                                    # the rest page
    tax_bill_or_not = True

    tax_bill_count = 0
    decl_form_count = 0
    tax_ID_count = 0
    tax_amount_count = 0

    tax_bill_entry = False          # 稅單資料輸入
    decl_form_entry = False         # 報單資料輸入
    tax_ID_entry = False            # 統一編號輸入
    tax_amount_entry = False        # 報單金額輸入
    #    es = class_set.entry_setting(tax_bill_entry, decl_form_entry, tax_ID_entry,
    #                    tax_amount_entry)
    es = class_set.entry_setting(tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry)
    # handling arguments and options
    # read input file name and output file name
    """
    try:
        # getopt.getopt(args, shortopts, longopts=[])
        opts, args = getopt.getopt(argv, "hi:o:t:", ["ifile=", "ofile=", "tfile="])
    except getopt.GetoptError:
        print("syntax: \n\tcustom_pdf_2_txt.py -i <inputfile> -t <textoutputfile> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("syntax: \n\tcustom_pdf_2_txt.py -i <inputfile> -t <textoutputfile> -o <outputfile>")
            sys.exit()
        elif opt in ("-i", "--ifile"):      # input .pdf file
            input_file = arg
        elif opt in ("-o", "--ofile"):      # output .csv file
            output_file = arg
        elif opt in ("-t", "--tfile"):      # intermediate .txt file
            textoutput_file = arg
    """
    # printing input/output/textoutput files
    if input_file != "":
        print("輸入彙總稅單清單名稱(pdf):", input_file)
        ifObj = open(input_file, "rb")
    else:
        print("請輸入彙總稅單清單名稱!")
        sys.exit()

    stripped_file_name = input_file[:len(input_file)-3]
    # intermediate .txt file
    if textoutput_file == "":
        textoutput_file = stripped_file_name + "text"
    print("彙總稅單文字內容(text):", textoutput_file)
    if os.path.isfile("./"+ textoutput_file):
#        print("彙總稅單文字內容 file exists!")
        os.remove("./"+ textoutput_file)

    tfObj = open(textoutput_file, "wb")
#    tfObj = sys.stdout

    # ultimate .csv output
    stripped_file_name = input_file[:len(input_file)-3]
    if output_file == "":
        output_file = stripped_file_name + "txt"
    print("彙總稅單清單轉出名稱(tab separated)", output_file)
    ofObj = open(output_file, "w", encoding="utf-8")

    all_texts = None
    detect_vertical = None
    word_margin = None
    char_margin = None
    line_margin = None
    boxes_flow = None
    strip_control = False
    output_type = 'text'
    layoutmode = 'normal'

    laparams = pdfminer.layout.LAParams()
    for param in ("all_texts", "detect_vertical", "word_margin", "char_margin", "line_margin", "boxes_flow"):
            paramv = locals().get(param, None)
            if paramv is not None:
                setattr(laparams, param, paramv)

    pdfminer.high_level.extract_text_to_fp(ifObj, tfObj, **locals())
    tfObj.close()

#    tfObj.seek(0, 0)

    if __debug__ is False:
        dbgFileObj = open("debug_output.txt", "w", encoding="utf-8")

#    pdb.set_trace()

    tfObj.close()

    tfObj = open(textoutput_file, "r", encoding="utf-8")
    print_flag = False
    # reading input file line-by-line
    tfStr = tfObj.readline()

    while tfStr:
        # for x in tfStr:
        #    print(x.encode("utf-8").decode("utf-8", "ignore"))
        #
        # determining the state of entries
        #
#        if tfStr.strip("\n") == constant.FILE_HEADER:
        if tfStr.strip('\n') == constant.FILE_HEADER:
            # 彙總稅單稅單清單
            if __debug__ is False:
                print("File Header: ", tfStr.strip('\n'))
#        elif tfStr.strip('\n') == constant.FILE_TAILER:
            # 總筆數"
#            print("File Tailer: ", tfStr.strip('\n'))
        elif tfStr.strip('\n') == constant.BEGINNING_DECLARATION_ID:
            # 報單號碼
            print_flag = True
            tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry = \
                es.clear_current_setting()
            tax_bill_entry = True
            es.set_current_entry(tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry)
            if __debug__ is False:
                print("Beginning declaration ID: ", tfStr.strip('\n'))
#        elif tfStr.strip('\n') == constant.PAGE_TAILER:
            # 製表日期
#            print("Page Tailer: ", tfStr.strip('\n'))
        elif tfStr.strip('\n') == constant.BEGINNING_TAX_ID_COLUMN: # also END_DECLARATION_ID
            # 納稅義務人統編
            print_flag = True
            tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry = \
                es.clear_current_setting()
            tax_ID_entry = True
            es.set_current_entry(tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry)
            if __debug__ is False:
                print("Tax ID: ", tfStr.strip('\n'))
        elif tfStr.strip('\n') == constant.BEGINNING_AMOUNT_COLUMN:
            # 金額
            print_flag = True
            tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry = \
                es.clear_current_setting()
            tax_amount_entry = True
            es.set_current_entry(tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry)
            if __debug__ is False:
                print("Amount: ", tfStr.strip('\n'))
        elif tfStr.strip('\n') == constant.END_AMOUNT_COLUMN_P1:
            print_flag = True
            tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry = \
                es.clear_current_setting()
            if __debug__ is False:
                dbgFileObj.write("<<<<製表日期>>>>\n")
        elif tfStr[:2] == constant.END_TAX_ID_P2:
            print_flag = True
            tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry = \
                es.clear_current_setting()
            if __debug__ is False:
                dbgFileObj.write("<<<<頁碼>>>>\n")
        elif tfStr.strip('\n') == constant.RECORD_COUNT:
            print_flag = True
            tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry = \
                es.clear_current_setting()
            if __debug__ is False:
                dbgFileObj.write("<<<<總筆數>>>>\n")

        #
        # processing per state machine
        #
        valid_entry, tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry = \
            es.get_current_setting()
        # if print_flag is True:
        #    print_flag = False
        #    print(es.get_current_setting())

        # state machine processing column entries
        if tax_bill_entry is True:
            if print_flag is True:
                print_flag = False
#                print("處理稅單、報單資料")
                if __debug__ is False:
                    dbgFileObj.write(tfStr)
            else:
                if tfStr.strip('\n') != "":
                    if tax_bill_or_not is True:
                        tax_bill_list.append(tfStr.strip('\n'))
                        tax_bill_or_not = False
                    else:
                        declaration_form_list.append(tfStr.strip('\n'))
                        tax_bill_or_not = True
                    if __debug__ is False:
                        dbgFileObj.write(tfStr)
        elif tax_ID_entry is True:
            if print_flag is True:
                print_flag = False
#                print("處理統一編號")
                if __debug__ is False:
                    dbgFileObj.write(tfStr)
            else:
                if tfStr.strip('\n') != "":
                    tax_ID_list.append(tfStr.strip('\n'))
                    if __debug__ is False:
                        dbgFileObj.write(tfStr)
        elif tax_amount_entry is True:
            if print_flag is True:
                print_flag = False
#                print("金額")
                if __debug__ is False:
                    dbgFileObj.write(tfStr)
            else:
                if tfStr.strip('\n') != "":
                    tax_amount_list.append(tfStr.strip('\n'))
                    if __debug__ is False:
                        dbgFileObj.write(tfStr)

        tfStr = tfObj.readline()

    if __debug__ is False:
        dbgFileObj.write("tax_bill_list length:" + str(len(tax_bill_list)) + "\n")
        dbgFileObj.write("declaration_form_list:" + str(len(declaration_form_list)) + "\n")
        dbgFileObj.write("tax_ID_list:" + str(len(tax_ID_list)) + "\n")
        dbgFileObj.write("tax_amount_llist:" + str(len(tax_amount_list)) + "\n")
#
# compose output file by combining the four lists collected in
# the above statemachine
#
    if len(tax_bill_list) == len(declaration_form_list) == len(tax_ID_list) == \
        len(tax_amount_list):
        for i in range(0, len(tax_bill_list)):
            combined_string = declaration_form_list[i] + "\t" + tax_bill_list[i] + \
                            "\t" + tax_ID_list[i] + "\t" + tax_amount_list[i] + "\n"
            ofObj.write(combined_string)
        excel_output.generate_excel_output(stripped_file_name, tax_bill_list, declaration_form_list, tax_ID_list, tax_amount_list)

    if ifObj.closed is False:
        # print("Closing input file...")
        ifObj.close()

    if ofObj.closed is False:
        ofObj.close()

    if tfObj.closed is False:
        tfObj.close()

    if __debug__ is False:
        dbgFileObj.close()
