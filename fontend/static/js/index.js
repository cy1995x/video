console.log('外部js加载成功');
console.log(blogData);
console.log(faderData);

$(function(){
  // 当页面元素加载完成后执行的代码
  // 使用faderData在页面中加载所有的轮播图
  // 图片路径通常随着项目位置发生变化 尽量不要直接写死图片
  // 采用地址+图片名的方式拼接路径

  var BASE_URL = '../static/images/';
  // var BASE_URL = 'http://127.0.0.1:8000/';
  // 遍历faderData 生成三个li标签 添加到页面元素.fader_controls之前
  var html = '';
  $.each(faderData,function(i,o){
    html += `<li class="slide">
    <a href="#">
    <img src="${BASE_URL+o.img_url}">
    <span class="imginfo">
      ${o.img_info}
    </span>
    </a>
  </li>`
  })
  $('.fader_controls').before(html);
  // 调用 jquery.easyfader.min.js提供的轮播方法 实现图片切换效果
  $('.fader').easyFader();


  function add_blogs(data){
    var html = '';
    $.each(data,function(i,o){
      html += `<div class="blogs">
      <h3 class="blogtitle">
        <a href="#">
          ${o.blogtitle}
        </a>
      </h3>
      <div class="blogpic">
        <a href="#">
          <img src="${BASE_URL+o.blogpic}" alt="">
        </a>
      </div>
      <p class="blogtext">
        ${o.blogtext}
      </p>
      <ul>
        <li class="author"><a href="#">
        ${o.bloginfo.author}</a></li>
        <li class="lmname"><a href="#">
        ${o.bloginfo.lmname}</a></li>
        <li class="timer"><a href="#">
        ${o.bloginfo.timer}</a></li>
        <li class="view"><a href="#">
        ${o.bloginfo.view}</a></li>
        <li class="like"><a href="#">
        ${o.bloginfo.like}</a></li>
      </ul>
    </div>`
    })//遍历结束
    // 将拼接好的字符串添加到页面上
    $('.blogsbox').append(html);
  }

  // 先加载一部分博客内容
  // [0:4]
  add_blogs(blogData.slice(0,4));
  // 随着页面滚动 每次滚动条快要到底时 加载剩余内容
  // 滚动条滚动事件
  $(document).scroll(function(){
    // console.log('hello')
    // 完整文档高度(整个滚动条)
    var documentHeight = $(document).height();
    // 当前可视范围高度(滚动条滑块)
    var windowHeight = $(window).height();
    // 如果完整文档高度 大于当前可视范围高度 出现滚动条
    // 滚动条高度 (滚动条滑块从最上方向下移动的距离)
    var scrollTop = $(document).scrollTop();
    // 如果当前窗口可视范围高度+滚动条高度 = 完整文档高度时 说明滚动条到底了
    if(documentHeight - windowHeight - scrollTop<200){
      // 根据页面中已有的博客数量 获取后面4条数据
      // 页面有4条数据  slice(4,8) [4:8]
      // 页面8条数据    slice(8,12) [8:12]
      // 页面n条数据    slice(n,n+4)
      var size = $('.blogs').length;
      var data = blogData.slice(size,size+4);
      // 在页面上显示
      if(data.length>0){
        add_blogs(data)
      }
    }

  })

  






})