import React from 'react';
import { Card, Row, Col, Progress, Badge, Tag, Tooltip } from 'antd';
import { TrophyOutlined, FireOutlined, CrownOutlined } from '@ant-design/icons';

const Achievements: React.FC = () => {
  const achievements = [
    {
      id: 'first_person',
      title: 'Первый шаг',
      description: 'Добавьте вашу первую персону',
      icon: '👶',
      rarity: 'common',
      unlocked: true,
      progress: 100,
      points: 10
    },
    {
      id: 'archivist',
      title: 'Архивист',
      description: 'Добавьте 100+ персон в дерево',
      icon: '📚',
      rarity: 'rare',
      unlocked: false,
      progress: 45,
      points: 500,
      maxProgress: 100
    },
    {
      id: 'historian',
      title: 'Летописец',
      description: 'Найдите 5 различных веков',
      icon: '📖',
      rarity: 'epic',
      unlocked: false,
      progress: 3,
      points: 1000,
      maxProgress: 5
    },
    {
      id: 'connector',
      title: 'Связующий',
      description: 'Создайте 500+ связей',
      icon: '🔗',
      rarity: 'rare',
      unlocked: false,
      progress: 120,
      points: 750,
      maxProgress: 500
    },
    {
      id: 'detective',
      title: 'Сыщик',
      description: 'Найдите 10 совпадений',
      icon: '🔍',
      rarity: 'uncommon',
      unlocked: false,
      progress: 2,
      points: 250,
      maxProgress: 10
    },
    {
      id: 'legend',
      title: 'Легенда',
      description: 'Достигните уровня 20',
      icon: '👑',
      rarity: 'legendary',
      unlocked: false,
      progress: 7,
      points: 5000,
      maxProgress: 20
    }
  ];

  const rarityColor = {
    common: '#808080',
    uncommon: '#4169E1',
    rare: '#8B00FF',
    epic: '#FF8C00',
    legendary: '#FFD700'
  };

  return (
    <div>
      <h1>🏆 Достижения и квесты</h1>

      <Card title="📊 Статистика достижений" style={{ marginBottom: '24px' }}>
        <Row gutter={16}>
          <Col xs={12} sm={6}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '24px', fontWeight: 'bold' }}>8 / 25</div>
              <div>Разблокировано</div>
            </div>
          </Col>
          <Col xs={12} sm={6}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '24px', fontWeight: 'bold' }}>2,850</div>
              <div>Очков</div>
            </div>
          </Col>
          <Col xs={12} sm={6}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '24px', fontWeight: 'bold' }}>7</div>
              <div>Уровень</div>
            </div>
          </Col>
          <Col xs={12} sm={6}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '24px', fontWeight: 'bold' }}>35%</div>
              <div>До уровня 8</div>
            </div>
          </Col>
        </Row>
      </Card>

      <h2 style={{ marginTop: '32px' }}>🎯 Достижения</h2>
      <Row gutter={[16, 16]}>
        {achievements.map((achievement) => (
          <Col key={achievement.id} xs={24} sm={12} lg={8}>
            <Card
              hoverable
              style={{
                border: `2px solid ${rarityColor[achievement.rarity as keyof typeof rarityColor]}`,
                opacity: achievement.unlocked ? 1 : 0.7
              }}
            >
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '48px', marginBottom: '12px' }}>
                  {achievement.icon}
                </div>
                <h3>{achievement.title}</h3>
                <p style={{ color: '#666' }}>{achievement.description}</p>

                {achievement.unlocked ? (
                  <Tag color="green">✓ Разблокировано</Tag>
                ) : (
                  <>
                    <Progress
                      type="circle"
                      percent={Math.round((achievement.progress / achievement.maxProgress!) * 100)}
                      width={80}
                      style={{ margin: '12px auto' }}
                    />
                    <div style={{ fontSize: '12px', color: '#999' }}>
                      {achievement.progress} / {achievement.maxProgress}
                    </div>
                  </>
                )}

                <Tag
                  color={rarityColor[achievement.rarity as keyof typeof rarityColor]}
                  style={{ marginTop: '12px' }}
                >
                  {achievement.points} 🎖️
                </Tag>
              </div>
            </Card>
          </Col>
        ))}
      </Row>

      <h2 style={{ marginTop: '32px' }}>📋 Активные квесты</h2>
      <Row gutter={[16, 16]}>
        <Col xs={24}>
          <Card>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h3>🔍 Найди своих предков</h3>
                <p>Найдите информацию о 3 предках в архивах (1/3)</p>
              </div>
              <div style={{ textAlign: 'right' }}>
                <Progress type="circle" percent={33} width={60} />
                <div style={{ marginTop: '8px' }}>+100 🎖️</div>
              </div>
            </div>
          </Card>
        </Col>

        <Col xs={24}>
          <Card>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h3>📅 Столетний документ</h3>
                <p>Найдите запись, которой больше 100 лет (0/1)</p>
              </div>
              <div style={{ textAlign: 'right' }}>
                <Progress type="circle" percent={0} width={60} />
                <div style={{ marginTop: '8px' }}>+50 🎖️</div>
              </div>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Achievements;
