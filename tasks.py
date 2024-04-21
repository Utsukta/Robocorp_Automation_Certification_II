from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive


sel= Selenium()
@task
def order_robots_from_RobotSpareBin():
     """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
     open_robot_order_website()
     download_orders_file()
     close_annoying_modal()
     orders = get_orders()
     for order in orders:
          fill_the_form(order) 
          click_preview()
          screenshot_robot(order['Order number'])
          click_order()
          store_receipt_as_pdf(order['Order number'])
          embed_screenshot_to_receipt(order['Order number'])
          order_another()
          close_annoying_modal()
     
     archive_receipts()
     
#Step 1: Open the robot order website
def open_robot_order_website():
     sel.open_available_browser("https://robotsparebinindustries.com/#/robot-order")

#Step 2: Download CSV orders files
def download_orders_file():
     http= HTTP()
     http.download("https://robotsparebinindustries.com/orders.csv",overwrite=True)

#Step 3: Read the csv file into tables and returning orders
def get_orders():
     tables=Tables()
     table=tables.read_table_from_csv("orders.csv")
     return table

#Step 4: To click on OK when site opens 
def close_annoying_modal():
     """to get rid of that annoying modal that 
     pops up when you open 
     the robot order website"""
     sel.click_button('//*[@id="root"]/div/div[2]/div/div/div/div/div/button[1]')

def fill_the_form(order):
     sel.select_from_list_by_value('//*[@id="head"]',order['Head'])
     sel.click_element(f'//*[@id="id-body-{order["Body"]}"]')
     sel.input_text('//*[@placeholder="Enter the part number for the legs"]', order['Legs'])
     sel.input_text('//*[@id="address"]', order['Address'])

def click_preview():
    sel.scroll_element_into_view('//*[@id="preview"]')
    sel.click_button('//*[@id="preview"]')

def order_another():
     sel.click_button('//*[@id="order-another"]')

def click_order():
     sel.click_button('//*[@id="order"]')
     while sel.is_element_visible('//div[@class="alert alert-danger"]'):
          sel.scroll_element_into_view('//*[@id="order"]')
          sel.click_button('//*[@id="order"]')

def screenshot_robot(order_number):
    return sel.screenshot(locator='//*[@id="robot-preview-image"]',filename=f"output/screenshot/{order_number}.png")

def store_receipt_as_pdf(order_number):
     """Export the data to a pdf file"""
     receipt_html=(sel.find_element('//*[@id="receipt"]')).get_attribute('innerHTML')
     pdf=PDF()
     return pdf.html_to_pdf(receipt_html,f"output/receipt/{order_number}.pdf")
 

def embed_screenshot_to_receipt(order_number):
     pdf=PDF()
     pdf.add_watermark_image_to_pdf(
        image_path=f"output/screenshot/{order_number}.png",
        source_path=f"output/receipt/{order_number}.pdf",
        output_path=f"output/receipt/{order_number}.pdf",
    )

#Why do we prefer ZIP though? When you run your robots in Control Room 
#and get access to the robot output artifacts (such as the files the robot generates),
# you store the files in the output directory. Since Control Room does not support 
#subdirectories for the output artifacts, you need to ZIP the receipt PDFs.
     
def archive_receipts():
     archieve= Archive()
     archieve.archive_folder_with_zip("output/receipt","output/receipt.zip")













