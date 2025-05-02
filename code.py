import string
import re
import os
import chardet
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas

def analyze_text(file_path):
    # Sprawdzenie czy podany plik istnieje
    if not os.path.isfile(file_path):
        print("Błąd: Podany plik nie istnieje.")
        return

    # Sprawdzenie czy podany plik jest plikiem tekstowym
    if not is_text_file(file_path):
        print("Błąd: Podany plik nie jest plikiem tekstowym.")
        return

    # Inicjalizacja słowników częstości występowania znaków
    char_frequency = {}
    word_frequency = {}
    sentence_frequency = {}

    # Inicjalizacja liczników
    total_chars = 0
    total_words = 0
    total_sentences = 0

    # Odczytanie kodowania pliku
    file_encoding = detect_encoding(file_path)

    # Otwieranie pliku tekstowego z odpowiednim kodowaniem
    with open(file_path, 'r', encoding=file_encoding) as file:
        # Odczytanie zawartości pliku
        text = file.read()

        # Przetwarzanie tekstu znak po znaku
        for char in text:
            # Pomijanie znaków niebędących literami
            if char not in string.ascii_letters:
                continue

            # Aktualizacja częstości występowania znaków
            char = char.lower()
            if char in char_frequency:
                char_frequency[char] += 1
            else:
                char_frequency[char] = 1

            # Zliczanie łącznej liczby znaków
            total_chars += 1

        # Przetwarzanie tekstu po słowach
        words = re.findall(r'\b\w+\b', text)
        for word in words:
            # Aktualizacja częstości występowania słów
            word = word.lower()
            if word in word_frequency:
                word_frequency[word] += 1
            else:
                word_frequency[word] = 1

            # Zliczanie łącznej liczby słów
            total_words += 1

        # Przetwarzanie tekstu po zdaniach
        sentences = re.split(r'(?<=[.!?])\s+', text)
        for sentence in sentences:
            # Pomijanie zdań składających się tylko z znaków interpunkcyjnych
            if re.match(r'^[.!?]+\s*$', sentence):
                continue

            # Aktualizacja częstości występowania zdań
            if sentence in sentence_frequency:
                sentence_frequency[sentence] += 1
            else:
                sentence_frequency[sentence] = 1

            # Zliczanie łącznej liczby zdań
            total_sentences += 1

    # Sortowanie słowników częstości alfabetycznie
    sorted_char_frequency = sorted(char_frequency.items())
    sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
    sorted_sentence_frequency = sorted(sentence_frequency.items(), key=lambda x: x[1], reverse=True)

    # Wyświetlanie wyników
    print("Statystyki znaków:")
    for char, frequency in sorted_char_frequency:
        print(f"Znak: {char}, Częstość: {frequency}, Procent: {frequency / total_chars * 100:.2f}%")

    print("\nStatystyki słów:")
    for word, frequency in sorted_word_frequency:
        print(f"Słowo: {word}, Częstość: {frequency}, Procent: {frequency / total_words * 100:.2f}%")

    print("\nStatystyki zdań:")
    for sentence, frequency in sorted_sentence_frequency:
        print(f"Zdanie: {sentence}, Częstość: {frequency}, Procent: {frequency / total_sentences * 100:.2f}%")

    print("\nLiczba znaków:", total_chars)
    print("Liczba słów:", total_words)
    print("Liczba zdań:", total_sentences)

    # Zapis wyników analizy do pliku PDF
    output_file_path = os.path.splitext(file_path)[0] + "_report.pdf"
    generate_pdf_report(output_file_path, sorted_char_frequency, sorted_word_frequency, sorted_sentence_frequency,
                        total_chars, total_words, total_sentences)

    print("Analiza zakończona. Wyniki zostały zapisane do pliku {}.".format(output_file_path))

def is_text_file(file_path):
    text_file_extensions = ['.txt', '.text']
    file_extension = os.path.splitext(file_path)[1]
    return file_extension.lower() in text_file_extensions

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def generate_pdf_report(output_file_path, sorted_char_frequency, sorted_word_frequency, sorted_sentence_frequency,
                        total_chars, total_words, total_sentences):
    c = canvas.Canvas(output_file_path)
    c.setFont("Helvetica", 12)

    c.drawString(100, 700, "Statystyki znaków:")
    y = 680
    for char, frequency in sorted_char_frequency:
        text = f"Znak: {char}, Częstość: {frequency}, Procent: {frequency / total_chars * 100:.2f}%"
        c.drawString(100, y, text)
        y -= 20

    c.drawString(100, y-40, "Statystyki słów:")
    y -= 60
    for word, frequency in sorted_word_frequency:
        text = f"Słowo: {word}, Częstość: {frequency}, Procent: {frequency / total_words * 100:.2f}%"
        c.drawString(100, y, text)
        y -= 20

    c.drawString(100, y-40, "Statystyki zdań:")
    y -= 60
    for sentence, frequency in sorted_sentence_frequency:
        text = f"Zdanie: {sentence}, Częstość: {frequency}, Procent: {frequency / total_sentences * 100:.2f}%"
        c.drawString(100, y, text)
        y -= 20

    c.drawString(100, y-40, f"Liczba znaków: {total_chars}")
    c.drawString(100, y-60, f"Liczba słów: {total_words}")
    c.drawString(100, y-80, f"Liczba zdań: {total_sentences}")

    c.save()

# Przykładowe użycie funkcji analyze_text
file_path = 'sample1.txt'  # Ścieżka do pliku tekstowego

if is_text_file(file_path):
    encoding = detect_encoding(file_path)
    if encoding:
        print(f"Kodowanie wykryte: {encoding}")
        analyze_text(file_path)  # Poprawka: Usunięcie argumentu 'encoding'
    else:
        print("Nie można wykryć kodowania pliku.")
else:
    print("Podany plik nie jest plikiem tekstowym.")
