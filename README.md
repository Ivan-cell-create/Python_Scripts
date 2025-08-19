# Python_Scripts — Коллекция Python-скриптов

## 📚 Описание

Этот репозиторий содержит набор Python-скриптов для автоматизации различных задач, работы с файлами и сетями. Каждый скрипт реализует отдельную функциональность и может использоваться как самостоятельно, так и в составе более сложных проектов.

## 📁 Структура репозитория

- **Automation** — скрипты для автоматизации, например, мониторинг и перезапуск процессов  
- **Working_with_files** — инструменты для работы с файлами, конвертации и обработки  
- **socket** — сетевые утилиты, включая тест скорости интернета и диагностику

## 🚀 Как начать

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/Ivan-cell-create/Python_Scripts.git

    Перейдите в нужную папку, например:

cd Python_Scripts/Automation

Запустите скрипт:

    python Monitoring_and_restart.py

    Убедитесь, что у вас установлен Python 3.x и все необходимые зависимости.

🧩 Пример использования

Скрипт Monitoring_and_restart.py следит за состоянием процесса и при его отсутствии перезапускает его.

python Monitoring_and_restart.py --process_name "my_service"

🧪 Тестирование

Рекомендуется использовать unittest для модульного тестирования. Пример для Monitoring_and_restart.py:

import unittest
from unittest.mock import patch
from Monitoring_and_restart import check_process, restart_process

class TestProcessMonitoring(unittest.TestCase):

    @patch('Monitoring_and_restart.check_process')
    def test_process_not_found(self, mock_check):
        mock_check.return_value = False
        result = restart_process("my_service")
        self.assertEqual(result, "Process my_service not found. Attempting to restart.")

    @patch('Monitoring_and_restart.check_process')
    def test_process_found(self, mock_check):
        mock_check.return_value = True
        result = restart_process("my_service")
        self.assertEqual(result, "Process my_service is running.")

if __name__ == '__main__':
    unittest.main()

📄 Лицензия

Проект лицензирован под MIT License. Подробнее в файле LICENSE

📬 Обратная связь

Если у вас есть вопросы или предложения — создавайте issue или присылайте pull request.
