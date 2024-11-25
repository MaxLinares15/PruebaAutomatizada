import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Configuración del WebDriver
def get_driver():
    options = Options()
    options.headless = False  # Cambiar a True si no deseas ver la ejecución en pantalla
    driver_path = "C:\drivers\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Captura de pantalla en cada paso
def take_screenshot(driver, test_name):
    screenshot_path = f"tests/screenshots/{test_name}_{int(time.time())}.png"
    driver.save_screenshot(screenshot_path)

# Historia 1: Verificar carga de la página principal de YouTube
def test_homepage_load():
    driver = get_driver()
    driver.get("https://www.youtube.com")
    assert "YouTube" in driver.title
    take_screenshot(driver, "homepage_load")
    driver.quit()

# Historia 2: Realizar búsqueda de un video
def test_search_video():
    driver = get_driver()
    driver.get("https://www.youtube.com")
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys("Selenium tutorial")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)  # Esperar a que carguen los resultados
    results = driver.find_elements(By.ID, "video-title")
    assert len(results) > 0
    take_screenshot(driver, "search_video")
    driver.quit()

# Historia 3: Poner el primer video que aparezca al realizar la búsqueda
def test_play_first_video():
    driver = get_driver()
    driver.get("https://www.youtube.com")
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys("Selenium tutorial")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)  # Esperar a que carguen los resultados
    first_video = driver.find_element(By.XPATH, "//ytd-video-renderer//a[@id='video-title']")
    first_video.click()
    time.sleep(3)  # Esperar a que cargue el video
    assert "YouTube" in driver.title  # Verificar que se cargó la página de video
    take_screenshot(driver, "play_first_video")
    driver.quit()

# Historia 4: volver a la pagina principal
def test_search_video_and_return_home():
    driver = get_driver()
    driver.get("https://www.youtube.com")
    
    # Buscar un video
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys("Selenium tutorial")
    search_box.send_keys(Keys.RETURN)
    
    time.sleep(2)  # Esperar a que carguen los resultados
    first_video = driver.find_element(By.XPATH, "//ytd-video-renderer//a[@id='video-title']")
    first_video.click()
    
    # Esperar a que el video cargue y luego regresar a la página principal
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "video")))
    time.sleep(2)  # Dejar que el video cargue brevemente
    
    # Volver a la página principal de YouTube
    driver.get("https://www.youtube.com")
    
    # Verificar que se ha vuelto a la página principal
    assert "YouTube" in driver.title
    take_screenshot(driver, "search_video_and_return_home")
    driver.quit()


# Historia 5: pausar video
def test_pause_video():
    driver = get_driver()
    driver.get("https://www.youtube.com")
    
    # Buscar un video de tutoriales
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys("Selenium tutorial")
    search_box.send_keys(Keys.RETURN)
    
    time.sleep(2)  # Esperar a que carguen los resultados
    first_video = driver.find_element(By.XPATH, "//ytd-video-renderer//a[@id='video-title']")
    first_video.click()
    
    # Pausar el video después de cargarlo
    video_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "video")))
    driver.execute_script("arguments[0].pause();", video_element)  # Pausar el video usando JavaScript
    
    time.sleep(1)  # Esperar para asegurarse de que el video se ha pausado
    take_screenshot(driver, "pause_video")
    driver.quit()


# Ejecución de todas las pruebas
if __name__ == "__main__":
    pytest.main()
