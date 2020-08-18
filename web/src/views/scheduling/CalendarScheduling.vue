<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">日历排产</span>
      </div>
      <div class="platformContainer">
        <el-form :inline="true">
            <el-form-item>
                <el-date-picker v-model="dateselected" type="month" placeholder="选择月" size='small'></el-date-picker>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSubmit" icon='el-icon-s-promotion' size='small'>排产</el-button>
            </el-form-item>
        </el-form>
        <tableView class="" :tableData="PermissionTableData" @getTableData="getPermissionTable"></tableView>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
  export default {
    components:{tableView},
    data(){
      return {
        PermissionTableData:{
          tableName:"scheduledate",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"WorkDate",label:"日期",type:"input",value:""},
            {prop:"DateType",label:"类型",type:"input",value:""},
            {prop:"comment",label:"注释",type:"input",value:""},
            {prop:"color",label:"颜色",type:"input",value:""},
          ],
          data:[],
          limit:5,
          offset:1,
        },
        dateselected:'2020-04'
      }
    },
    created(){
      this.getPermissionTable()
    },
    methods:{
      getPermissionTable(){
        var that = this
        var params = {
          tableName: this.PermissionTableData.tableName,
          limit:this.PermissionTableData.limit,
          offset:this.PermissionTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.PermissionTableData.data = data.rows
            that.PermissionTableData.total = data.total
          }
        },res =>{
          console.log("请求错误")
        }
        )
      },
      getSchedule(){
          var params={

          }
          
      },
      synchronizeToWMS(){
         alert('同步物料到WMS')
      },
      synchronizeToPrepareSection(){
         alert('同步物料到备料段')
      },

    }
  }
</script>

<style scoped>

</style>