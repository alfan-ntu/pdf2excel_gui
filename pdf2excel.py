import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from datetime import datetime


class Pdf2Excel():
    def __init__(self):
        self.gladefile = "./glade/pdf2excel_gui.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")
        self.create_textview_log()
        self.window.show()

    def create_textview_log(self):
        self.text_buffer = Gtk.TextBuffer()
        self.textview_log = self.builder.get_object("textview_log")
        self.textview_log.set_buffer(self.text_buffer)
        self.textview_log.set_editable(False)

    def on_button_quit_clicked(self, widget, data=None):
        print("Quit with cancel")
        Gtk.main_quit()

    def on_button_convert_file_clicked(self, widget, data=None):
        log_content = "Convert File button clicked"
        self.log_buffer(log_content)

    def on_button_select_file_clicked(self, widget, data=None):
        self.fcd = Gtk.FileChooserDialog(title="選取檔案...",
                   parent=None,
                   action=Gtk.FileChooserAction.OPEN)
        self.fcd.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.fcd.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        self.fcd.set_default_size(300, 200)
        self.create_filechooser_filter()
        self.response = self.fcd.run()
        if self.response == Gtk.ResponseType.OK:
            log_content = "Selected file path: " + self.fcd.get_filename()
            self.log_buffer(log_content)
            self.fcd.destroy()
        else:
            self.fcd.destroy()

    # added a file filter to the file chooser dialog
    def create_filechooser_filter(self):
        pdf_filter = Gtk.FileFilter()
        pdf_filter.add_mime_type("application/pdf")
        pdf_filter.set_name("*.pdf 檔案")
        self.fcd.add_filter(pdf_filter)

        txt_filter = Gtk.FileFilter()
        txt_filter.add_mime_type("text/plain")
        txt_filter.set_name("*.txt 文字檔案")
        self.fcd.add_filter(txt_filter)

        excel_filter = Gtk.FileFilter()
        excel_filter.add_mime_type("application/vnd.ms-excel")
        excel_filter.add_mime_type("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        excel_filter.set_name("*.xlsx Excel 檔案")
        self.fcd.add_filter(excel_filter)

        any_filter = Gtk.FileFilter()
        any_filter.add_pattern("*.*")
        any_filter.set_name("所有檔案")
        self.fcd.add_filter(any_filter)

    # log utility, attach time stamp to log_content
    def log_buffer(self, log_content):
        datetimeObj = datetime.now()
        timestamp = str(datetimeObj.year) + "/" + str(datetimeObj.month) + "/" + str(datetimeObj.day) \
                    + " " + str(datetimeObj.hour) + ":" + str(datetimeObj.minute) + ":" + str(datetimeObj.second) \
                    + ">>> "
        log_content = timestamp + log_content
        buffer1 = self.text_buffer
        end_iter = buffer1.get_end_iter()
        buffer1.insert(end_iter, log_content + "\n")

if __name__ == "__main__":
    main = Pdf2Excel()
    Gtk.main()
