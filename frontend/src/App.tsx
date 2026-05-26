import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Layout, Menu, Avatar, Badge, Dropdown, Button } from 'antd';
import { UserOutlined, HomeOutlined, SearchOutlined, TrophyOutlined, LogoutOutlined } from '@ant-design/icons';

import Dashboard from './pages/Dashboard';
import FamilyTree from './pages/FamilyTree';
import Search from './pages/Search';
import Achievements from './pages/Achievements';
import Profile from './pages/Profile';

const { Header, Sider, Content, Footer } = Layout;

const App: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);
  const [user, setUser] = useState({
    id: 'user_123',
    name: 'Иван Петров',
    email: 'ivan@example.com',
    avatar: 'IP',
    level: 7,
    points: 850
  });

  const menuItems = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: <Link to="/">Главная</Link>
    },
    {
      key: '/tree',
      icon: <HomeOutlined />,
      label: <Link to="/tree">Мое дерево</Link>
    },
    {
      key: '/search',
      icon: <SearchOutlined />,
      label: <Link to="/search">Поиск</Link>
    },
    {
      key: '/achievements',
      icon: <TrophyOutlined />,
      label: <Link to="/achievements">Достижения</Link>
    },
    {
      key: '/profile',
      icon: <UserOutlined />,
      label: <Link to="/profile">Профиль</Link>
    }
  ];

  const userMenuItems = [
    {
      key: 'profile',
      label: 'Профиль',
      icon: <UserOutlined />
    },
    {
      key: 'logout',
      label: 'Выход',
      icon: <LogoutOutlined />,
      danger: true
    }
  ];

  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Sider
          trigger={null}
          collapsible
          collapsed={collapsed}
          style={{
            overflow: 'auto',
            height: '100vh',
            position: 'fixed',
            left: 0,
            top: 0,
            bottom: 0,
          }}
        >
          <div style={{ padding: '16px', textAlign: 'center', color: 'white' }}>
            <h2>🌳 Семейные корни</h2>
          </div>
          <Menu
            theme="dark"
            mode="inline"
            defaultSelectedKeys={['/']}
            items={menuItems}
          />
        </Sider>

        <Layout style={{ marginLeft: collapsed ? 80 : 200 }}>
          <Header
            style={{
              background: '#fff',
              padding: '0 16px',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}
          >
            <Button
              type="text"
              icon={collapsed ? '>>' : '<<'}
              onClick={() => setCollapsed(!collapsed)}
            />

            <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
              <Badge count={user.level} style={{ backgroundColor: '#52c41a' }}>
                <span>{user.points} 🎖️</span>
              </Badge>

              <Dropdown menu={{ items: userMenuItems }}>
                <Avatar icon={<UserOutlined />} size="large" style={{ cursor: 'pointer' }}>
                  {user.avatar}
                </Avatar>
              </Dropdown>
            </div>
          </Header>

          <Content style={{ margin: '16px' }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/tree" element={<FamilyTree />} />
              <Route path="/search" element={<Search />} />
              <Route path="/achievements" element={<Achievements />} />
              <Route path="/profile" element={<Profile />} />
            </Routes>
          </Content>

          <Footer style={{ textAlign: 'center' }}>
            © 2024 Семейные корни. Все права защищены.
            <br />
            <a href="https://familyroots.ru/about">О проекте</a>
            {' | '}
            <a href="https://familyroots.ru/privacy">Приватность</a>
            {' | '}
            <a href="https://familyroots.ru/terms">Условия</a>
          </Footer>
        </Layout>
      </Layout>
    </Router>
  );
};

export default App;
