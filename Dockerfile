FROM python:3.11-alpine
RUN mkdir /finance_level_bot
WORKDIR /finance_level_bot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]