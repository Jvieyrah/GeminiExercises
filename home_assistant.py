# home_assistant.py
def set_light_values(brightness: int, color_temperature: str) -> dict:
    """
    Ajusta a luminosidade e a temperatura de cor das luzes.
    """
    print("modificou as luzes")
    # Simula o ajuste de luzes
    return {"brightness": brightness, "color_temperature": color_temperature}
def intruder_alert() -> dict:
    """
    Ativa o alerta de intruso.
    """
    print("Ativou o alerta de intrusos")
    # Simula o alerta de intruso
    return {"alert": "Intruder alert activated"}
def start_music(energetic: bool, loud: bool, tempo: int) -> dict:
    """
    Inicia a reprodução de música com as características especificadas.
    """
    print("Reproduz musicas")
    # Simula o início da música
    return {"energetic": energetic, "loud": loud, "tempo": tempo}
def good_morning() -> dict:
    """
    Executa a rotina matinal.
    """
    print("Inicia a rotina matinal")
    # Simula a rotina matinal
    return {"routine": "Good morning routine started"}

def set_thermostat_temperature(temperature: float) -> dict:
    """
    define uma temperatura mais baixa ou mais alta.
    """
    print(f"a temperatura foi setada em {temperature} graus")
    return {"new temperature": temperature }

def open_curtains() -> dict:
    """
    Abre as cortinas para permitir passagem de luz.
    """
    print("As cortinas foram abertas")
    return {"Cortinas": "Abertas" }


__all__ = ["set_light_values", "intruder_alert", "start_music", "good_morning", "set_thermostat_temperature", "open_curtains"]