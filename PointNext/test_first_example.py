import time
import sys
import os
import pytest
from logUtil import logger
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BROWSER_WAIT = 3


def click_the_link(browser, link_name=None):
    if not link_name:
        link_name = "Case Status"
    logger.info("Link to be clicked '%s'" % link_name)
    link_xpath = "//*[contains(text(), '{0}')]".format(link_name)
    browser.find_element_by_xpath(link_xpath).click()
    time.sleep(BROWSER_WAIT)


def process_chatbot_chat(recorded_conv, browser):

    logger.info("Recorded Chat to be verified: \n%s " % recorded_conv)
    chatbot_fresh_chat = retrieve_chat_info(browser)

    for conversation in recorded_conv.split("\n"):
        conversation = conversation.replace("\n", "")
        if conversation == 'Exit':
            break
        conv_user_text = conversation.split(">")

        if len(conv_user_text) == 2:
            conv_user = conv_user_text[0].strip()
            conv_text = conv_user_text[1].strip()
        else:
            break

        if 'Bot'.lower() in conv_user.lower():
            chatbot_text = chatbot_fresh_chat['texts']
            chatbot_text = ''.join(chatbot_text)
            assert conv_text in chatbot_text,\
                "Bot recorded chat '{0}' not present in Chatbot text '{1}'".format(conv_text, chatbot_text)
        elif 'Clicks On'.lower() in conv_user.lower() or 'Buttons'.lower() in conv_user.lower():
            chatbot_button_text = chatbot_fresh_chat['buttons']
            conv_buttons = conv_text.strip().split(',')
            for conv_button in conv_buttons:
                if conv_button.strip() not in chatbot_button_text:
                    assert False, "Recorded button text '{0}' not present in Chatbot buttons list '{1}'".format(
                        conv_button.strip(), str(chatbot_button_text))
                if 'Clicks On'.lower() in conv_user.lower():
                    click_the_link(browser, conv_button)
                    time.sleep(BROWSER_WAIT)
                    chatbot_fresh_chat = retrieve_chat_info(browser)
                    break
        else:
            chatbot_button_text = chatbot_fresh_chat['buttons']
            assert not chatbot_button_text, "Buttons %s are still present even when chatbot is waiting for User input "\
                                            %  str(chatbot_button_text)
            user_input_area = browser.find_elements_by_xpath("//*[@class='inputHelperWrapper']")
            for field in user_input_area:
                textarea = field.find_element_by_tag_name("textarea")
                textarea.clear()
                textarea.send_keys(conv_text.strip())
                field.find_element_by_tag_name("button").click()
            get_refresh_element(browser)
            chatbot_fresh_chat = retrieve_chat_info(browser)

def get_refresh_element(browser):
    wrapper_right_count = browser.find_elements_by_class_name("wrapperRight")
    if wrapper_right_count:
        chat_data = browser.find_elements_by_xpath("//div[@class='wrapperRight'][last()]/following-sibling::div")
        # chat_data = latest_chat_data.find_elements_by_xpath("//following-sibling::div")
    else:
        chat_data = browser.find_elements_by_xpath("//div[@class='wrapperLeft']")
    for chats in chat_data:
        refresh_stale_element("text", chats)
        refresh_stale_element("horizontalButton", chats)
    return chat_data

def retrieve_chat_info(browser):

    chat_data = get_refresh_element(browser)
    chatbot_current_data = {}
    texts = []
    buttons = []
    for chats in chat_data:
        chatbot_texts = refresh_stale_element("text", chats)
        for sub_text in chatbot_texts:
            chatbot_text = sub_text.text
            if not chatbot_text:
                sub_chatbot_text = sub_text.find_elements_by_xpath("//div/descendant::*/div")
                for sub_sub_text in sub_chatbot_text:
                    sub_bot_text = sub_sub_text.text
                    texts.append(sub_bot_text)
            else:
                texts.append(chatbot_text)

        chatbot_button = refresh_stale_element("horizontalButton", chats)
        if chatbot_button:
            chatbot_texts = chats.find_elements_by_xpath("//*[@class='horizontalButton']/button")
            for button in chatbot_texts:
                buttons.append(button.text)

    chat_data.clear()
    logger.info("Text retrieved from Chatbot '%s' " % ''.join(texts))
    chatbot_current_data['texts'] = texts

    logger.info("Buttons seen in the Chatbot '%s' " % str(buttons))
    chatbot_current_data['buttons'] = buttons
    return chatbot_current_data


def refresh_stale_element(element, browser):
    retry = 10
    chatbot_texts = None
    while True:
        try:
            chatbot_texts = browser.find_elements_by_class_name(element)
            break
        except StaleElementReferenceException:
            retry -= 1
            time.sleep(BROWSER_WAIT)
            if not retry:
                logger.error("Could not able to refresh '%s' " % element)
                break
        except NoSuchElementException:
            break
    return chatbot_texts


def test_file(user_data, click_chatbot):

    process_chatbot_chat(user_data, click_chatbot)


if __name__ == "__main__":

    file_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(file_dir, 'chat_data.txt')

    file = open(filepath, 'r')
    lines = []
    file_data_l = []
    for line in file.readlines():
        if line == '\n':
            if lines:
                file_data_l.append(''.join(lines[:]))
            lines = []
        else:
            lines.append(line)
    if lines:
        if ''.join(lines[:]) not in file_data_l:
            file_data_l.append(''.join(lines[:]))
    file.close()
    for index, file_data in enumerate(file_data_l):
        logger.info("\n++++++++++++ Testing Scenario %d ++++++++++++" % (index+1))
        pytest.main([__file__, "--user_data", str(file_data), "-v"])
        logger.info("\n++++++++++++ Done Scenario %d ++++++++++++" % (index+1))
