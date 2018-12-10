import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from Building import Building

# logs in, manages the game and closes the browser
def executeGameSession(settings):
    # setup web browser
    browser = webdriver.Chrome('.\\chromedriver.exe',)
    loginAndSelectWorld(browser, settings['player'])

    if (settings['player']['reapVillages']):
        reapVillages(browser)
    if (settings['player']['manageSenate']):
        manageSenate(browser, settings['buildings'])

    browser.quit()


# go to all available villages and reaps resources
def reapVillages(browser):
    #go to island view
    goToIslandViewButton = browser.find_element_by_class_name('island_view')
    goToIslandViewButton.click()
    time.sleep(1)
    pressEscape(browser)
    time.sleep(1)

    # reap all villages that are available
    while len(browser.find_elements_by_class_name('claim')) > 0:
        pressEscape(browser)
        # open village window
        villageLink = browser.find_element_by_class_name('claim')
        actions = ActionChains(browser)
        actions.move_to_element(villageLink).click().perform()
        time.sleep(1)

        # make sure we're allowed to collect resources
        if len(browser.find_element_by_class_name('pb_bpv_unlock_time').text) == 0:
            # click on button to collect resources
            collectResourcesButtons = browser.find_elements_by_class_name('card_click_area')
            collectResourcesButtons[1].click()
            time.sleep(1)
            pressEscape(browser)
            time.sleep(1)

        # close village window
        pressEscape(browser)
        time.sleep(1)


# logs the user in and navigates to the game world
def loginAndSelectWorld(browser, player):
    browser.maximize_window()
    browser.get('https://us.grepolis.com/')
    time.sleep(2)

    # find username and password inputs
    usernameInput = browser.find_element_by_id('login_userid')
    passwordInput = browser.find_element_by_id('login_password')

    # enter user name and password
    usernameInput.send_keys(player['username'])
    time.sleep(1)
    passwordInput.send_keys(player['password'])
    time.sleep(1)

    #press login button
    loginButton = browser.find_element_by_id('login_Login')
    loginButton.click()
    time.sleep(1)

    #select world
    index = player['worldIndex']
    worldButton = browser.find_elements_by_class_name('world_name')[index]
    worldButton.find_element_by_css_selector('div').click()
    time.sleep(2)
    
    # exit any pop ups
    pressEscape(browser)
    time.sleep(1)
    pressEscape(browser)


def goToSenateScreen(browser):
    # go to the city overview
    browser.find_element_by_class_name('city_overview').click()
    time.sleep(1)
    
    warCoinBox = browser.find_element_by_class_name('war_coins_box')
    actions = ActionChains(browser)
    actions.move_to_element(warCoinBox).move_by_offset(-440, 0).click().perform()
    time.sleep(1)


def manageSenate(browser, buildingSettings):
    
    goToSenateScreen(browser)
    buildings = buildingArray(browser, buildingSettings)
    if (len(buildings) > 0):
        # upgradge building whose furthest from goal
        buildingToUpgrade = min(buildings, key = lambda x: x.percentToGoal())
        buildingToUpgrade.htmlButton.click()
    
    time.sleep(1)
    pressEscape(browser)
    time.sleep(0.4)
    pressEscape(browser)
    time.sleep(1)


def buildingArray(browser, buildingSettings):
    
    allButtons = browser.find_elements_by_class_name('build_up')
    buildings = []

    k = 0
    while k < len(buildingSettings):
        newBuilding = Building(buildingSettings[k], allButtons[k])
        if newBuilding.haveEnoughResources:
            buildings.append(newBuilding)
        k += 1

    return buildings


def pressEscape(browser):
    browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)