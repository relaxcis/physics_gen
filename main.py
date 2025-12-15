# main.py
from flask import Flask, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def calculate_kinematics(v0, a, t):
    """Рассчитывает пройденный путь и генерирует данные для графика."""
    
    # 1. Расчет пути: S = v0*t + 0.5*a*t^2
    distance = v0 * t + 0.5 * a * (t ** 2)
    
    # 2. Генерация данных для графика скорости v(t) = v0 + a*t
    time_points = np.linspace(0, t, 100)
    velocity_points = v0 + a * time_points
    
    # 3. Создание графика
    fig, ax = plt.subplots()
    ax.plot(time_points, velocity_points, label=f'v(t) = {v0} + {a}t')
    ax.set_title('График скорости v(t)')
    ax.set_xlabel('Время (с)')
    ax.set_ylabel('Скорость (м/с)')
    ax.grid(True)
    
    # Сохранение графика в памяти и кодирование в base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig) # Закрываем, чтобы не занимать память
    plot_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return distance, plot_base64

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    v0 = data.get('v0')
    a = data.get('a')
    t = data.get('t')
    
    try:
        distance, plot_base64 = calculate_kinematics(v0, a, t)
        return jsonify({
            'distance': distance,
            'plot_base64': plot_base64
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Запуск сервера Flask
    app.run(debug=True)