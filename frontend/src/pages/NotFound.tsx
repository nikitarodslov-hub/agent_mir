import React from 'react';
import { Button, Result } from 'antd';

const NotFound: React.FC = () => {
  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #1890ff 0%, #52c41a 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      <Result
        status="404"
        title={<span style={{ color: 'white' }}>404</span>}
        subTitle={<span style={{ color: 'rgba(255,255,255,0.8)' }}>Страница не найдена</span>}
        extra={
          <div style={{ textAlign: 'center' }}>
            <p style={{ color: 'rgba(255,255,255,0.8)', marginBottom: '16px' }}>
              Извините, страница, которую вы ищете, не существует.
            </p>
            <Button type="primary" size="large" href="/" style={{ background: 'white', color: '#1890ff' }}>
              На главную
            </Button>
          </div>
        }
      />
    </div>
  );
};

export default NotFound;
