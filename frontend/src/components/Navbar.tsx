import React, { useState } from 'react';
import { Menu, Button, Dropdown, Avatar, Space, Drawer, Row, Col } from 'antd';
import { MenuOutlined, LoginOutlined, UserAddOutlined, UserOutlined, LogoutOutlined } from '@ant-design/icons';
import { useLocation, useNavigate } from 'react-router-dom';

const Navbar: React.FC = () => {
  const [drawerVisible, setDrawerVisible] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const isLoggedIn = false; // Mock auth state

  const menuItems = [
    { label: 'Главная', key: '/', href: '/' },
    { label: 'О нас', key: '/about', href: '/about' },
    { label: 'Цены', key: '/pricing', href: '/pricing' },
    { label: 'FAQ', key: '/faq', href: '/faq' },
    { label: 'Контакты', key: '/contact', href: '/contact' }
  ];

  const userMenuItems = [
    {
      key: 'profile',
      label: 'Мой профиль',
      icon: <UserOutlined />,
      onClick: () => navigate('/account')
    },
    {
      type: 'divider'
    },
    {
      key: 'logout',
      label: 'Выход',
      icon: <LogoutOutlined />,
      onClick: () => {
        // Logout logic
        navigate('/');
      }
    }
  ];

  return (
    <>
      <div style={{
        background: 'white',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        padding: '0 20px',
        position: 'sticky',
        top: 0,
        zIndex: 100
      }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: '64px' }}>
          {/* Logo */}
          <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#1890ff', cursor: 'pointer' }} onClick={() => navigate('/')}>
            🌳 Семейные корни
          </div>

          {/* Desktop Menu */}
          <div style={{ display: 'none' }}>
            {/* Will be shown on desktop */}
          </div>

          <div style={{ display: 'flex' }}>
            <Menu
              mode="horizontal"
              selectedKeys={[location.pathname]}
              style={{
                border: 'none',
                display: 'flex'
              }}
              items={menuItems.map(item => ({
                key: item.key,
                label: <a href={item.href} style={{ textDecoration: 'none', color: 'inherit' }}>{item.label}</a>
              }))}
            />
          </div>

          {/* Right side actions */}
          <Space size="middle" style={{ marginLeft: '20px' }}>
            {!isLoggedIn ? (
              <>
                <Button type="text" onClick={() => navigate('/login')}>
                  <LoginOutlined /> Вход
                </Button>
                <Button type="primary" onClick={() => navigate('/register')}>
                  <UserAddOutlined /> Регистрация
                </Button>
              </>
            ) : (
              <>
                <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
                  <Avatar style={{ background: '#1890ff', cursor: 'pointer' }}>
                    И
                  </Avatar>
                </Dropdown>
              </>
            )}
            <Button
              type="text"
              icon={<MenuOutlined />}
              onClick={() => setDrawerVisible(true)}
              style={{ display: 'none' }}
            />
          </Space>
        </div>
      </div>

      {/* Mobile Drawer */}
      <Drawer
        title="Меню"
        placement="left"
        onClose={() => setDrawerVisible(false)}
        open={drawerVisible}
      >
        <Menu
          mode="vertical"
          selectedKeys={[location.pathname]}
          items={menuItems.map(item => ({
            key: item.key,
            label: <a href={item.href} onClick={() => setDrawerVisible(false)}>{item.label}</a>
          }))}
        />
        <div style={{ marginTop: '20px', display: 'flex', gap: '10px' }}>
          {!isLoggedIn ? (
            <>
              <Button type="default" block onClick={() => { navigate('/login'); setDrawerVisible(false); }}>
                Вход
              </Button>
              <Button type="primary" block onClick={() => { navigate('/register'); setDrawerVisible(false); }}>
                Регистрация
              </Button>
            </>
          ) : null}
        </div>
      </Drawer>
    </>
  );
};

export default Navbar;
