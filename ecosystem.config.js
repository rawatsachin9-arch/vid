module.exports = {
  apps: [
    {
      name: 'videoai-backend',
      script: './backend/venv/bin/uvicorn',
      args: 'server:app --host 127.0.0.1 --port 8001',
      cwd: '/home/videoai/videoai-app/backend',
      env: {
        NODE_ENV: 'production',
        PYTHONPATH: '/home/videoai/videoai-app/backend'
      },
      env_file: '/home/videoai/videoai-app/backend/.env.production',
      instances: 1,
      exec_mode: 'fork',
      watch: false,
      max_memory_restart: '1G',
      error_file: '/home/videoai/logs/backend-error.log',
      out_file: '/home/videoai/logs/backend-out.log',
      log_file: '/home/videoai/logs/backend-combined.log',
      time: true,
      autorestart: true,
      restart_delay: 1000,
      max_restarts: 10,
      min_uptime: '10s'
    }
  ]
};