import os
import time

from PIL import Image


def __driverExcute(driver, scripts: list):
    total_width = driver.execute_script(scripts[0])
    total_height = driver.execute_script(scripts[1])
    viewport_width = driver.execute_script(scripts[2])
    viewport_height = driver.execute_script(scripts[3])
    return (total_width, total_height, viewport_width, viewport_height)


def screenshot_by_id(driver, id, file):
    scriptList = ['return document.getElementById("{id}").offsetWidth'.format(id=id),
                  'return document.getElementById("{id}").parentNode.scrollHeight'.format(id=id),
                  'return document.getElementById("{id}").clientWidth'.format(id=id),
                  'return window.innerHeight'.format(id=id)
                  ]
    scriptList = ['return document.body.offsetWidth',
                  'return document.body.parentNode.scrollHeight',
                  'return document.body.clientWidth',
                  'return window.innerHeight'
                  ]
    scripts = __driverExcute(driver, scriptList)
    return __save_screenshotScollOnlyHeight(driver, id, file, scripts)


def fullpage_screenshot(driver, file):
    scriptList = ['return document.body.offsetWidth',
                  'return document.body.parentNode.scrollHeight',
                  'return document.body.clientWidth',
                  'return window.innerHeight'
                  ]
    scripts = __driverExcute(driver, scriptList)
    return __divid_screenshot(driver, file, scripts)


def __save_screenshotScollOnlyHeight(driver, id, file, scripts):
    total_width, total_height, viewport_width, viewport_height = scripts
    # log("Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height,viewport_width,viewport_height))
    rectangles = []
    element = driver.find_element_by_id(id)
    location = element.location
    size = element.size

    i = 0
    while i < total_height:
        ii = 0
        top_height = i + viewport_height

        if top_height > total_height:
            top_height = total_height

        while ii < total_width:
            top_width = ii + viewport_width

            if top_width > total_width:
                top_width = total_width

            # log("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
            rectangles.append((ii, i, top_width, top_height))

            ii = ii + viewport_width

        i = i + viewport_height

    stitched_image = Image.new('RGB', (total_width, total_height))
    previous = None
    part = 0

    for rectangle in rectangles:
        if not previous is None:
            driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
            # log("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
            time.sleep(0.2)

        file_name = file + "_part_{0}.png".format(part)
        # log("Capturing {0} ...".format(file_name))

        driver.get_screenshot_as_file(file_name)
        screenshot = Image.open(file_name)

        if rectangle[1] + viewport_height > total_height:
            offset = (rectangle[0], total_height - viewport_height)
        else:
            offset = (rectangle[0], rectangle[1])

        # log("Adding to stitched image with offset ({0}, {1})".format(offset[0],offset[1]))
        stitched_image.paste(screenshot, offset)

        del screenshot
        os.remove(file_name)
        part = part + 1
        previous = rectangle

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    stitched_image = stitched_image.crop((left, top, right, bottom))
    stitched_image.save(file)
    # log("Finishing chrome full page screenshot workaround...")
    return True


def __divid_screenshot(driver, file, scripts):
    # log("Starting chrome full page screenshot workaround ...")

    total_width, total_height, viewport_width, viewport_height = scripts
    # log("Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height,viewport_width,viewport_height))
    rectangles = []

    i = 0
    while i < total_height:
        ii = 0
        top_height = i + viewport_height

        if top_height > total_height:
            top_height = total_height

        while ii < total_width:
            top_width = ii + viewport_width

            if top_width > total_width:
                top_width = total_width

            # log("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
            rectangles.append((ii, i, top_width, top_height))

            ii = ii + viewport_width

        i = i + viewport_height

    stitched_image = Image.new('RGB', (total_width, total_height))
    previous = None
    part = 0

    for rectangle in rectangles:
        if not previous is None:
            driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
            # log("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
            time.sleep(0.2)

        file_name = file + "_part_{0}.png".format(part)
        # log("Capturing {0} ...".format(file_name))

        driver.get_screenshot_as_file(file_name)
        screenshot = Image.open(file_name)

        if rectangle[1] + viewport_height > total_height:
            offset = (rectangle[0], total_height - viewport_height)
        else:
            offset = (rectangle[0], rectangle[1])

        # log("Adding to stitched image with offset ({0}, {1})".format(offset[0],offset[1]))
        stitched_image.paste(screenshot, offset)

        del screenshot
        os.remove(file_name)
        part = part + 1
        previous = rectangle

    stitched_image.save(file)
    # log("Finishing chrome full page screenshot workaround...")
    return True
