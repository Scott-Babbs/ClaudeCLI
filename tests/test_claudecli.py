import pytest
from unittest.mock import patch, MagicMock
from Models.claudecli import main, display_loading_indicator
from threading import Event
from io import StringIO

def test_display_loading_indicator():
    with patch('sys.stdout', new=StringIO()) as fake_output:
        stop_event = Event()
        display_loading_indicator(stop_event)
        stop_event.set()
        expected_output = "thinking...\r          \r"
        assert fake_output.getvalue() == expected_output

    with patch('sys.stdout', new=StringIO()) as fake_output:
        stop_event = Event()
        stop_event.set()
        display_loading_indicator(stop_event)
        assert fake_output.getvalue() == ""

    with patch('sys.stdout', new=StringIO()) as fake_output:
        stop_event = Event()
        with patch('time.sleep', return_value=None):
            display_loading_indicator(stop_event, duration=0.5)
            stop_event.set()
        assert "thinking..." in fake_output.getvalue()

    with patch('sys.stdout', new=StringIO()) as fake_output:
        stop_event = Event()
        with pytest.raises(KeyboardInterrupt):
            with patch('time.sleep', side_effect=KeyboardInterrupt):
                display_loading_indicator(stop_event)
        assert "thinking..." in fake_output.getvalue()

    with patch('sys.stdout', new=StringIO()) as fake_output:
        stop_event = Event()
        display_loading_indicator(stop_event)
        stop_event.set()
        assert fake_output.getvalue().endswith("\r          \r")

def test_main_valid_input(monkeypatch):
    user_input = "What is the capital of France?"
    expected_output = "The capital of France is Paris."
    
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(content=expected_output)
    monkeypatch.setattr('anthropic.Anthropic', lambda *args, **kwargs: mock_client)
    
    with patch('builtins.print') as mock_print:
        main()
        mock_print.assert_called_with(f"Assistant: {expected_output}")

def test_main_invalid_input(monkeypatch):
    user_input = ""
    expected_output = "Type 'quit' to exit the conversation."
    
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    
    with patch('builtins.print') as mock_print:
        main()
        mock_print.assert_called_with(expected_output)

def test_main_api_error(monkeypatch):
    user_input = "What is the capital of France?"
    
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    mock_client = MagicMock()
    mock_client.messages.create.side_effect = Exception("API Error")
    monkeypatch.setattr('anthropic.Anthropic', lambda *args, **kwargs: mock_client)
    
    with patch('builtins.print') as mock_print:
        with pytest.raises(Exception):
            main()