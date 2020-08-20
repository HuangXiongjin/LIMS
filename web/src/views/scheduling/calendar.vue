<template>
  <el-row :gutter="20">
    <el-col :span="24">
      <div class="platformContainer blackComponents">
        <FullCalendar :plugins="calendarPlugins"
                      :droppable="true"
                      locale="zh-cn"
                      :header="header"
                      :events="events"
                      :height="800"
                      :editable="true"
                      :selectable="true"
                      :button-text="buttonText"
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
  export default {
    name: "calendar",
    components:{FullCalendar},
    data(){
      return {
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
      this.getScheduling()
    },
    methods:{
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
    }
  }
</script>

<style scoped>

</style>
