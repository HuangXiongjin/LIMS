<template>
  <el-row :gutter="20">
    <el-col :span="5">
      <div class="scheduleContainer" style="height: 630px;">
        <div id='external-events' class="marginBottom">
          <h4>可拖放需要插单的品名</h4>
          <el-input v-model="productName" placeholder="请输入品名" @change="handleChangeProductName"></el-input>
          <a class='fc-event' v-for="item in results" style="padding: 5px;margin: 10px 0;cursor: pointer;">{{item.BrandName}}</a>
        </div>
      </div>
    </el-col>
    <el-col :span="19">
      <div class="platformContainer blackComponents">
        <FullCalendar :plugins="calendarPlugins"
                      :droppable="true"
                      locale="zh-cn"
                      :header="header"
                      :events="events"
                      :height="600"
                      :editable="true"
                      :selectable="true"
                      :button-text="buttonText"
                      @dateClick="handleDateClick"
                      @eventClick="handleEventClick"
                      @eventDrop="handleEventDrop"
                      @drop="drop"
        />
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import FullCalendar from '@fullcalendar/vue'
  import dayGridPlugin from "@fullcalendar/daygrid";
  import timeGridPlugin from "@fullcalendar/timegrid";
  import interactionPlugin, { Draggable } from "@fullcalendar/interaction";
  import '@fullcalendar/core/main.css';
  import '@fullcalendar/daygrid/main.css';
  import '@fullcalendar/timegrid/main.css';
  var moment = require('moment');
  export default {
    name: "calendar",
    components:{FullCalendar},
    data(){
      return {
        scheduleTableData:[],
        results:[],
        productName:'',
        calendarPlugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
        events:[],
        buttonText:{
          today:'今天',
          month: '月',
          week: '周',
          day: '天'
        },
        header:{
          left:'prev,next today',
          center:'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
      }
    },
    mounted(){
      this.getScheduleTableData()
      this.getScheduling()
      new Draggable(document.getElementById("external-events"), {
        itemSelector: '.fc-event',
        eventData: function(eventEl) {
          return {
            title: eventEl.innerText,
          };
        }
      });
    },
    methods:{
      handleChangeProductName(queryString){
        if(queryString != ""){
          this.results = this.scheduleTableData.filter((string) =>{
            return Object.keys(string).some(function(key) {
              return String(string[key]).toLowerCase().indexOf(queryString) > -1
            })
          })
        }else{
          this.results = this.scheduleTableData
        }
      },
      getScheduleTableData(){ //获取可拖动的品名
        var that = this
        var params = {
          tableName: "ProductRule",
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.scheduleTableData = res.data.data.rows
            that.results = that.scheduleTableData
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      getScheduling(){  //获取日历所有日程
        let that = this
        that.axios.get("/api/CUID",{
          params: {
            tableName: "scheduledate",
            limit:100000000,
            offset:0
          }
        }).then(res =>{
          if(res.data.code === "200"){
            that.events = []
            res.data.data.rows.forEach(item =>{
              that.events.push({
                ID:item.ID,
                title:item.DateType,
                color:item.color,
                start:item.WorkDate
              })
            })
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      drop(e){
        let that = this
        var params = {
          tableName: "scheduledate",
          DateType:e.draggedEl.innerText,
          WorkDate:e.dateStr,
          color:e.draggedEl.attributes.color.value
        }
        that.axios.post("/api/CUID",that.qs.stringify(params)).then(res =>{
          if(res.data.code == "200"){
            that.$message({
              showClose: true,
              type: 'success',
              message: "添加成功"
            });
            that.getScheduling()
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      handleDateClick(e) {  //点击日期

      },
      handleEventClick(e){  //点击日历里的日程 进行删除
        let that = this
        var ID = {
          id:e.event.extendedProps.ID
        }
        that.$confirm('此操作将永久删除该日程, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          that.axios.delete("/api/CUID",{
            params: {
              tableName: "scheduledate",
              delete_data:JSON.stringify(ID),
            }
          }).then(res =>{
            if(res.data.code == "200"){
              that.$message({
                type: 'success',
                message: '删除成功!'
              });
              that.getScheduling()
            }
          },res =>{
            console.log("请求错误")
          })
        }).catch(() => {
          that.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      },
      handleEventDrop(e){ //日历里拖拽换位日程 进行修改
        let that = this
        var startDate = moment(e.event.start).format('YYYY-MM-DD')
        var params = {
          tableName: "scheduledate",
          ID:e.event.extendedProps.ID,
          DateType:e.event.title,
          WorkDate:startDate,
          color:e.event.backgroundColor
        }
        that.axios.put("/api/CUID",that.qs.stringify(params)).then(res =>{
          if(res.data.code == "200"){
            that.$message({
              showClose: true,
              type: 'success',
              message: '修改成功'
            });
            that.getScheduling()
          }else{
            that.$message({
              type: 'info',
              message: res.data
            });
          }
        })
      },
    }
  }
</script>

<style scoped>

</style>
