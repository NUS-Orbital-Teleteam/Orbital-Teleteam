import React from 'react';
import { Link } from 'react-router-dom';
import { Layout, Menu, Breadcrumb, PageHeader, Avatar } from 'antd';
import { UserOutlined, LaptopOutlined, SolutionOutlined } from '@ant-design/icons';

import { Profile } from '../components'
import SidebarGroup from '../components/SidebarGroup'

import './Layout.css';

const { SubMenu } = Menu;
const { Header, Footer, Sider, Content } = Layout;


class AppLayout extends React.Component {

    constructor (props) {
      super(props);
      this.state = {groups: props.groups};
    }

    sidebarGroups = () => {
      if (this.state.groups.length == 0){
        return <Menu.Item>You have no groups registered.</Menu.Item>
      }
      return this.state.groups.map( group => {
      return <Menu.Item key={group.id} onClick={this.props.updateGroups}>
          <Link to={`/group?id=${group.id}`}>
            <SidebarGroup group={group} />
          </Link>
        </Menu.Item>
    });
    }

    componentDidUpdate(prevProps) {
      if (prevProps.groups !== this.props.groups) {
        this.setState({groups : this.props.groups});
      }
    }

    render() {
    return (
    <div>
    <Layout>
    <Sider 
    width={300} 
    className="site-layout-background"
    breakpoint="xl"
    >
        
        <Menu
          mode="inline"
          defaultSelectedKeys={['987654321'] /* Random key, so that none is selected */ }
          defaultOpenKeys={['sub1']}
          style={{ height: '100%', borderRight: 0 }}
          theme="dark"
        > 
          <SubMenu key="profile" icon={<UserOutlined />} title="Profile">
            <Menu.Item className="user-profile-menu-item" style={{ height: '50px' }}>
              <Profile user={this.props.user} />
            </Menu.Item>
          </SubMenu>
          <SubMenu key="sub1" icon={<SolutionOutlined />} title="Your groups">
            {!this.state.groups ? 'Loading' : this.sidebarGroups()}
          </SubMenu>
          <SubMenu key="sub2" icon={<LaptopOutlined />} title="Account">
            <Menu.Item key="5"><Link to={"/settings"}>Settings</Link></Menu.Item>
            <Menu.Item key="6"><Link to={"/login"} onClick={this.props.onLogout}>Sign out</Link></Menu.Item>
          </SubMenu>
        </Menu>
      </Sider>
      <Layout className="site-layout">
          <Content style={{ margin: '0 16px' }}>
            <div className="site-layout-background" style={{ padding: 24, minHeight: 360 }}>
              { this.props.children }
            </div>
          </Content>
        </Layout>
    </Layout>
    </div>
    );
    }
}

export default AppLayout;