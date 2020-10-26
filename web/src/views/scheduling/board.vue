<template>
  <el-row>
    <el-col :span='24'>
      <el-row :gutter='20'>
        <el-col :span='16'>
          <div class="cardContainer">
            <div class="platformTitle">批计划状态统计图</div>
            <ve-waterfall :data="chartPlanData" :extend="chartPlanExtend" height="360px"></ve-waterfall>
          </div>
        </el-col>
        <el-col :span='8'>
          <div class="cardContainer">
            <div class="platformTitle">批计划待处理列表</div>
            <el-table :data="PlanTableData" border size="small" height="360px">
              <el-table-column prop="PlanNum" label="编号"></el-table-column>
              <el-table-column prop="BrandName" label="品名"></el-table-column>
              <el-table-column prop="PlanQuantity" label="计划产量"></el-table-column>
              <el-table-column prop="PlanStatus" label="计划状态">
                <template slot-scope="scope">
                  <span class="color-darkblue" v-if="scope.row.PlanStatus === '已下发'">{{ scope.row.PlanStatus }}</span>
                  <span class="color-orange" v-if="scope.row.PlanStatus === '待审核'">{{ scope.row.PlanStatus }}</span>
                  <span class="color-purple" v-if="scope.row.PlanStatus === '待配置'">{{ scope.row.PlanStatus }}</span>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name: "board",
    data(){
      return {
        chartPlanExtend:{
          grid: {
            top: 30,
            bottom:10
          },
          series:{
            barMaxWidth:50
          }
        },
        chartPlanData: {
          columns: ['状态', '数量'],
          rows: []
        },
        PlanTableData:[]
      }
    },
    mounted(){
      this.searchPlan()
    },
    methods:{
      searchPlan(){
        var that = this
        var params = {
          tableName:"PlanManager",
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            var PlanStatus1 = 0
            var PlanStatus2 = 0
            var PlanStatus3 = 0
            var PlanStatus4 = 0
            var PlanStatus5 = 0
            var PlanStatus6 = 0
            var PlanStatus7 = 0
            var PlanStatus8 = 0
            var PlanStatus9 = 0
            res.data.data.rows.forEach(item =>{
              if(item.PlanStatus === "新增"){
                PlanStatus1 = PlanStatus1 + 1
              }
              if(item.PlanStatus === "待审核"){
                PlanStatus2 = PlanStatus2 + 1
              }
              if(item.PlanStatus === "待下发"){
                PlanStatus3 = PlanStatus3 + 1
              }
              if(item.PlanStatus === "已下发"){
                PlanStatus4 = PlanStatus4 + 1
              }
              if(item.PlanStatus === "已发送投料计划"){
                PlanStatus5 = PlanStatus5 + 1
              }
              if(item.PlanStatus === "已发送物料明细"){
                PlanStatus6 = PlanStatus6 + 1
              }
              if(item.PlanStatus === "已选设备"){
                PlanStatus7 = PlanStatus7 + 1
              }
              if(item.PlanStatus === "执行"){
                PlanStatus8 = PlanStatus8 + 1
              }
              if(item.PlanStatus === "已完成"){
                PlanStatus9 = PlanStatus9 + 1
              }
              if(item.PlanStatus === "待审核" || item.PlanStatus === "待下发" || item.PlanStatus === "已下发"){
                that.PlanTableData.push(item)
              }
            })
            that.chartPlanData.rows = [
              {"状态":"新增","数量":PlanStatus1},
              {"状态":"待审核","数量":PlanStatus2},
              {"状态":"待下发","数量":PlanStatus3},
              {"状态":"已下发","数量":PlanStatus4},
              {"状态":"已发送投料计划","数量":PlanStatus5},
              {"状态":"已发送物料明细","数量":PlanStatus6},
              {"状态":"已选设备","数量":PlanStatus7},
              {"状态":"执行","数量":PlanStatus8},
              {"状态":"已完成","数量":PlanStatus9},
            ]
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
