#!/bin/bash
set -e

echo "========================================="
echo "🚀 Iniciando Lacrei Saúde API"
echo "========================================="

# Aguarde o banco de dados ficar pronto
echo "⏳ Aguardando banco de dados..."
while ! nc -z ${DB_HOST:-db} ${DB_PORT:-5432}; do
  sleep 1
done
echo "✅ Banco de dados pronto"

# Execute migrações
echo "📦 Executando migrações..."
python manage.py migrate

# Colete arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput || true

# Crie super usuário de desenvolvimento (opcional)
if [ "$DEBUG" = "True" ]; then
  echo "👤 Criando super usuário de desenvolvimento (se não existir)..."
  python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("✅ Super usuário criado: admin / admin")
else:
    print("ℹ️ Super usuário já existe")
END
fi

# Inicie servidor
echo "🔧 Iniciando servidor..."
python manage.py runserver 0.0.0.0:8000
