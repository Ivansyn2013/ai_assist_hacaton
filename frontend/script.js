// База данных ответов AI-пациента для острого аппендицита
// const patientResponses = {
//     'начало': 'Добрый день. У меня сильно болит живот.',
//     'боль': 'Сначала болел весь живот, сейчас больше справа внизу. Боль ноющая, постоянная.',
//     'где болит': 'Сначала болел весь живот, сейчас больше справа внизу. Боль ноющая, постоянная.',
//     'тошнота': 'Дважды была рвота, тошнит до сих пор. Боль началась около 12 часов назад.',
//     'рвота': 'Дважды была рвота, тошнит до сих пор.',
//     'температура': 'Да, 37.8°C.',
//     'аппетит': 'Аппетита нет вообще, даже пить не хочется.',
//     'симптом щеткина': 'Резкая боль при отпускании руки! 💥',
//     'анализы': 'Результаты: ОАК - лейкоциты 14.5×10⁹/л, нейтрофилез; УЗИ - утолщенный аппендикс 9 мм, жидкость вокруг.',
//     'сколько времени болит': 'Боль началась около 12 часов назад.',
//     'характер боли': 'Боль ноющая, постоянная, усиливается при движении.',
//     'стул': 'Стула не было сегодня, газы отходят.',
//     'что предпринимал': 'Пытался принять но-шпу, не помогло.',
//     'мочеиспускание': 'Мочеиспускание обычное, безболезненное.',
//     'аллергия': 'Аллергий нет.',
//     'операции': 'Раньше не оперировался.',
//     'хронические': 'Хронических заболеваний нет.'
// };

// Медицинские показатели
let medicalData = {
    temperature: '37.8°C',
    pressure: '130/85',
    pulse: '95 уд/мин',
    painLocation: 'Правая подвздошная область',
    symptoms: ['Боль в животе', 'Тошнота', 'Рвота', 'Лихорадка']
};

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', function () {
    updateMedicalPanel();

    // Первое сообщение пациента
    setTimeout(() => {
        addMessage(patientResponses['начало'], 'patient');
    }, 500);
});
// Fetch to backend
async function sendMessage() {
    const BACK_URL = ''
    const input = document.getElementById('messageInput');
    const message = input.value.trim();

    if (message) {
        addMessage(message, 'doctor');
        // processPatientResponse(message);
        input.value = '';
    }

    // Start spinner
    const spinner = document.getElementById('spinner');
    spinner.style.display = 'block';

    try {
        const response = await fetch(`${BACK_URL}/ai_request`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        if (!response.ok) {
            throw new Error('Ошибка сети или сервера');
        }

        const data = await response.json();

        // Добавляем ответ от AI-пациента
        addMessage(data.response, 'patient');

        // Опционально: обновляем медицинскую панель, если бэкенд прислал данные
        if (data.medicalData) {
            medicalData = data.medicalData;
            updateMedicalPanel();
        }
    } catch (error) {
        console.error('Ошибка при запросе к AI:', error);
        addMessage('❌ Не удалось получить ответ от сервера. Проверьте подключение.', 'patient');
    } finally {
        // Скрываем спинер
        spinner.style.display = 'none';
    }
}


function sendQuickMessage(message) {
    addMessage(message, 'doctor');
    processPatientResponse(message);
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function addMessage(text, sender) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;

    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);

    // Прокрутка вниз
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function processPatientResponse(doctorMessage) {
    const lowerMessage = doctorMessage.toLowerCase();
    let response = 'Не могли бы вы уточнить вопрос?';

    // Поиск подходящего ответа
    for (const [key, value] of Object.entries(patientResponses)) {
        if (lowerMessage.includes(key)) {
            response = value;
            break;
        }
    }

    // Обновление медицинских данных при определенных вопросах
    if (lowerMessage.includes('температур')) {
        medicalData.temperature = '37.8°C';
    }

    if (lowerMessage.includes('где болит') || lowerMessage.includes('локализация')) {
        medicalData.painLocation = 'Правая подвздошная область';
    }

    // Имитация задержки ответа AI
    setTimeout(() => {
        addMessage(response, 'patient');
        updateMedicalPanel();
    }, 1000);
}

function updateMedicalPanel() {
    document.getElementById('temp').textContent = medicalData.temperature;
    document.getElementById('pressure').textContent = medicalData.pressure;
    document.getElementById('pulse').textContent = medicalData.pulse;
    document.getElementById('painLocation').textContent = medicalData.painLocation;
}

function showFeedback() {
    document.getElementById('feedbackModal').style.display = 'flex';
}

function closeFeedback() {
    document.getElementById('feedbackModal').style.display = 'none';
}
