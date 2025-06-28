App({
  /**
   * 全局数据
   */
  globalData: {
    userInfo: null,
    hasLogin: false,
    // 服务器地址，实际应用中应该替换为真实的API地址
    apiBaseUrl: 'https://api.example.com',
    // 用户类型：student或teacher
    userType: '',
    systemInfo: null
  },

  /**
   * 当小程序初始化完成时，会触发 onLaunch（全局只触发一次）
   */
  onLaunch: function () {
    // 检查登录状态
    this.checkLoginStatus();

    // 获取系统信息
    const systemInfo = wx.getSystemInfoSync();
    this.globalData.systemInfo = systemInfo;

    // 检查更新
    this.checkUpdate();
  },

  /**
   * 检查登录状态
   */
  checkLoginStatus: function () {
    const token = wx.getStorageSync('token');
    const userType = wx.getStorageSync('userType');
    
    if (token) {
      // 更新全局状态
      this.globalData.userType = userType;
      
      // 获取用户信息
      const userInfo = wx.getStorageSync('userInfo');
      if (userInfo) {
        this.globalData.userInfo = userInfo;
      }
      
      // 注意：这里只是设置了全局状态，但没有立即判断为登录
      // 实际的登录状态验证在登录页面进行
      // 这样可以避免在应用启动时进行网络请求，提高启动速度
      
      // 只有在验证token有效后，才会在对应页面设置hasLogin=true
      this.globalData.hasLogin = false;
    }
  },

  /**
   * 登录方法
   */
  login: function (username, password, userType, callback) {
    // 显示加载中
    wx.showLoading({
      title: '登录中...',
    });

    // 实际应用中，这里应该请求服务器进行身份验证
    // 这里使用模拟数据
    setTimeout(() => {
      wx.hideLoading();
      
      // 模拟登录成功
      const token = 'mock_token_' + Date.now();
      const userInfo = {
        id: username,
        nickName: userType === 'student' ? '张同学' : '李老师',
        userType: userType
      };
      
      // 存储登录信息
      wx.setStorageSync('token', token);
      wx.setStorageSync('userType', userType);
      wx.setStorageSync('userInfo', userInfo);
      wx.setStorageSync('username', username);
      
      // 更新全局数据
      this.globalData.hasLogin = true;
      this.globalData.userInfo = userInfo;
      this.globalData.userType = userType;
      
      // 执行回调
      if (callback && typeof callback === 'function') {
        callback(true);
      }
    }, 1000);
  },

  /**
   * 退出登录
   */
  logout: function (callback) {
    // 清除存储的登录信息
    wx.removeStorageSync('token');
    wx.removeStorageSync('userType');
    wx.removeStorageSync('userInfo');
    wx.removeStorageSync('username');
    
    // 重置全局数据
    this.globalData.hasLogin = false;
    this.globalData.userInfo = null;
    this.globalData.userType = '';
    
    // 执行回调
    if (callback && typeof callback === 'function') {
      callback();
    }
  },

  /**
   * 检查小程序更新
   */
  checkUpdate: function () {
    if (wx.canIUse('getUpdateManager')) {
      const updateManager = wx.getUpdateManager();
      updateManager.onCheckForUpdate(function (res) {
        if (res.hasUpdate) {
          updateManager.onUpdateReady(function () {
            wx.showModal({
              title: '更新提示',
              content: '新版本已准备好，是否重启应用？',
              success: function (res) {
                if (res.confirm) {
                  updateManager.applyUpdate();
                }
              }
            });
          });
          
          updateManager.onUpdateFailed(function () {
            wx.showModal({
              title: '更新提示',
              content: '新版本下载失败，请检查网络后重试',
              showCancel: false
            });
          });
        }
      });
    }
  }
})
