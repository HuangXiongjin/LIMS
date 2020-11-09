<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <div class="page-title">
        <span class="text-size-16">物料发送历史记录</span>
      </div>
      <div class="platformContainer">
        <el-form :inline="true">
          <el-form-item label="发送时间">
            <el-date-picker type="date" v-model="OperationDate" size="mini" format="yyyy-MM-dd" style="width: 140px;" :clearable="false" @change="getMaterialTableData"></el-date-picker>
          </el-form-item>
          <el-form-item class="floatRight">
            <el-radio-group v-model="SendFlag" size="small" @change="getMaterialTableData">
              <el-radio-button label="投料系统已接收"></el-radio-button>
              <el-radio-button label="投料系统已接收退料"></el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-form>
        <el-table :data="MaterialTableData.data" border size="small">
          <el-table-column type="selection"></el-table-column>
          <el-table-column prop="BatchID" label="批次号"></el-table-column>
          <el-table-column prop="BrandName" label="品名"></el-table-column>
          <el-table-column prop="MATName" label="物料名称"></el-table-column>
          <el-table-column prop="BucketNum" label="桶号"></el-table-column>
          <el-table-column prop="BucketWeight" label="重量"></el-table-column>
          <el-table-column prop="Unit" label="单位"></el-table-column>
          <el-table-column prop="Flag" label="桶/托盘标识"></el-table-column>
          <el-table-column prop="SendFlag" label="物料状态"></el-table-column>
          <el-table-column prop="OperationDate" label="发送时间"></el-table-column>
        </el-table>
        <div class="paginationClass">
          <el-pagination background  layout="total, sizes, prev, pager, next, jumper"
           :total="MaterialTableData.total"
           :current-page="MaterialTableData.offset"
           :page-sizes="[5,10,20]"
           :page-size="MaterialTableData.limit"
           @size-change="handleSizeChange"
           @current-change="handleCurrentChange">
          </el-pagination>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "sendMaterialLog",
    data(){
      return {
        MaterialTableData:{
          data:[],
          limit: 5,
          offset: 1,
          total: 0,
        },
        OperationDate:moment().format("YYYY-MM-DD"),
        SendFlag:"投料系统已接收",
      }
    },
    mounted(){
      this.getMaterialTableData()
    },
    methods:{
       getMaterialTableData(){
        var that = this
        var params = {
          tableName: "BatchMaterialInfo",
          OperationDate:this.OperationDate,
          SendFlag: this.SendFlag,
          limit:this.MaterialTableData.limit,
          offset:this.MaterialTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.MaterialTableData.data = res.data.data.rows
            that.MaterialTableData.total = res.data.data.total
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      handleSizeChange(limit){ //每页条数切换
        this.PlanManagerTableData.limit = limit
        this.getMaterialTableData()
      },
      handleCurrentChange(offset) { // 页码切换
        this.PlanManagerTableData.offset = offset
        this.getMaterialTableData()
      },
    }
  }
</script>

<style scoped>

</style>
