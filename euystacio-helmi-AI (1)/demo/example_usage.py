from core.euystacio_core import EuystacioCore
from spi.sentimento_pulse_interface import analyze_pulse
from tutor.tutor_nomination import nominate

core = EuystacioCore()
pulse = analyze_pulse("Love and trust under the storm")
print("Pulse:", pulse)
print("Evolved state:", core.evolve(pulse))
print("Tutor nominations:", nominate())
