import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Layout, Menu, Avatar, Badge, Dropdown, Button } from 'antd';
import { UserOutlined, HomeOutlined, SearchOutlined, TrophyOutlined, LogoutOutlined } from '@ant-design/icons';

import Dashboard from './pages/Dashboard';
import FamilyTree from './pages/FamilyTree';
import Search from './pages/Search';
import Achievements from './pages/Achievements';
import Profile from './pages/Profile';
import LandingPage from './pages/LandingPage';
import Pricing from './pages/Pricing';
import About from './pages/About';
import Contact from './pages/Contact';
import FAQ from './pages/FAQ';
import Terms from './pages/Terms';
import Privacy from './pages/Privacy';
import Account from './pages/Account';
import NotFound from './pages/NotFound';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

const { Header, Sider, Content } = Layout;

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

  const isPublicPage = (pathname: string) => {
    return ['/landing', '/pricing', '/about', '/contact', '/faq', '/terms', '/privacy', '/'].includes(pathname);
  };

  return (
    <Router>
      <Routes>
        {/* Public pages with Navbar and Footer */}
        <Route path="/" element={<><Navbar /><LandingPage /><Footer /></>} />
        <Route path="/landing" element={<><Navbar /><LandingPage /><Footer /></>} />
        <Route path="/pricing" element={<><Navbar /><Pricing /><Footer /></>} />
        <Route path="/about" element={<><Navbar /><About /><Footer /></>} />
        <Route path="/contact" element={<><Navbar /><Contact /><Footer /></>} />
        <Route path="/faq" element={<><Navbar /><FAQ /><Footer /></>} />
        <Route path="/terms" element={<><Navbar /><Terms /><Footer /></>} />
        <Route path="/privacy" element={<><Navbar /><Privacy /><Footer /></>} />

        {/* Authenticated pages with sidebar */}
        <Route path="/dashboard" element={
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
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/tree" element={<FamilyTree />} />
                  <Route path="/search" element={<Search />} />
                  <Route path="/achievements" element={<Achievements />} />
                  <Route path="/profile" element={<Profile />} />
                  <Route path="/account" element={<Account />} />
                </Routes>
              </Content>
            </Layout>
          </Layout>
        } />

        {/* Legacy authenticated routes */}
        <Route path="/tree" element={
          <Layout style={{ minHeight: '100vh' }}>
            <Sider trigger={null} collapsible collapsed={collapsed}
              style={{ overflow: 'auto', height: '100vh', position: 'fixed', left: 0, top: 0, bottom: 0 }}>
              <div style={{ padding: '16px', textAlign: 'center', color: 'white' }}><h2>🌳 Семейные корни</h2></div>
              <Menu theme="dark" mode="inline" defaultSelectedKeys={['/tree']} items={menuItems} />
            </Sider>
            <Layout style={{ marginLeft: collapsed ? 80 : 200 }}>
              <Header style={{ background: '#fff', padding: '0 16px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Button type="text" icon={collapsed ? '>>' : '<<'} onClick={() => setCollapsed(!collapsed)} />
                <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                  <Badge count={user.level} style={{ backgroundColor: '#52c41a' }}><span>{user.points} 🎖️</span></Badge>
                  <Dropdown menu={{ items: userMenuItems }}><Avatar icon={<UserOutlined />} size="large" style={{ cursor: 'pointer' }}>{user.avatar}</Avatar></Dropdown>
                </div>
              </Header>
              <Content style={{ margin: '16px' }}><FamilyTree /></Content>
            </Layout>
          </Layout>
        } />

        <Route path="/search" element={
          <Layout style={{ minHeight: '100vh' }}>
            <Sider trigger={null} collapsible collapsed={collapsed}
              style={{ overflow: 'auto', height: '100vh', position: 'fixed', left: 0, top: 0, bottom: 0 }}>
              <div style={{ padding: '16px', textAlign: 'center', color: 'white' }}><h2>🌳 Семейные корни</h2></div>
              <Menu theme="dark" mode="inline" defaultSelectedKeys={['/search']} items={menuItems} />
            </Sider>
            <Layout style={{ marginLeft: collapsed ? 80 : 200 }}>
              <Header style={{ background: '#fff', padding: '0 16px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Button type="text" icon={collapsed ? '>>' : '<<'} onClick={() => setCollapsed(!collapsed)} />
                <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                  <Badge count={user.level} style={{ backgroundColor: '#52c41a' }}><span>{user.points} 🎖️</span></Badge>
                  <Dropdown menu={{ items: userMenuItems }}><Avatar icon={<UserOutlined />} size="large" style={{ cursor: 'pointer' }}>{user.avatar}</Avatar></Dropdown>
                </div>
              </Header>
              <Content style={{ margin: '16px' }}><Search /></Content>
            </Layout>
          </Layout>
        } />

        <Route path="/achievements" element={
          <Layout style={{ minHeight: '100vh' }}>
            <Sider trigger={null} collapsible collapsed={collapsed}
              style={{ overflow: 'auto', height: '100vh', position: 'fixed', left: 0, top: 0, bottom: 0 }}>
              <div style={{ padding: '16px', textAlign: 'center', color: 'white' }}><h2>🌳 Семейные корни</h2></div>
              <Menu theme="dark" mode="inline" defaultSelectedKeys={['/achievements']} items={menuItems} />
            </Sider>
            <Layout style={{ marginLeft: collapsed ? 80 : 200 }}>
              <Header style={{ background: '#fff', padding: '0 16px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Button type="text" icon={collapsed ? '>>' : '<<'} onClick={() => setCollapsed(!collapsed)} />
                <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                  <Badge count={user.level} style={{ backgroundColor: '#52c41a' }}><span>{user.points} 🎖️</span></Badge>
                  <Dropdown menu={{ items: userMenuItems }}><Avatar icon={<UserOutlined />} size="large" style={{ cursor: 'pointer' }}>{user.avatar}</Avatar></Dropdown>
                </div>
              </Header>
              <Content style={{ margin: '16px' }}><Achievements /></Content>
            </Layout>
          </Layout>
        } />

        {/* Account page */}
        <Route path="/account" element={<><Navbar /><Account /><Footer /></>} />

        {/* 404 Page */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
};

export default App;
