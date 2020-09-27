<template>
  <el-row :gutter="15">
    <el-col :span="4">
         <div class="platformContainer">
            <p class="marginBottom">选择要查询的品名</p>
            <el-input class="marginBottom" v-model="productName" placeholder="关键字搜索" @change="handleChangeProductName"></el-input>
            <el-tag class="marginBottom marginRight cursor-pointer" v-for="(item,index) in results" :key="index" v-bind:effect="item.BrandName===BrandActive?'dark':'plain'" @click="clickBrandTag(item.BrandName,item.BrandCode)">{{item.BrandName}}</el-tag>
          </div>
    </el-col>
    <el-col :span='20'>
        <div class="platformContainer">
              <p>当前选择的品名：{{BrandActive}}</p>
        </div>
        <div class="platformContainer">
              <el-table
                  :data="planTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  ref="multipleTable"
                  @selection-change="handleSelectionChange" 
                  @row-click="TabCurrentChange"
                  style="width: 100%">
                  <el-table-column type="selection"></el-table-column>
                  <el-table-column v-for="item in tableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="planTableData.total"
                  :current-page="planTableData.offset"
                  :page-size="planTableData.limit"
                  @size-change="handleSizeChange"
                  @current-change="handleCurrentChange">
                  </el-pagination>
            </div>
        </div>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    name:"ElectronicBatchRecord",
    data(){
      return {
        productName:'',
        results:[],
        BrandActive:'',
        tableconfig:[{prop:'BatchID',label:"批次号"},{prop:'BrandCode',label:'品名编码'},{prop:'BrandName',label:'品名'},{prop:'PlanStatus',label:'计划状态'},{prop:'PlanBeginTime',label:'计划开始时间'},{prop:'PlanEndTime',label:'计划开始时间'}],
        planTableData:{
          tableName:"PlanManager",
          data:[],
          limit: 10,//当前显示多少条
          offset: 1,//当前处于多少页
          total: 0,//总的多少页
        },
        currentBatch:{},
        multipleSelection:[],
        currentBrandBatch:[]
      }
    },
    created(){
      this.getScheduleTableData()
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
       clickBrandTag(BrandName,BrandCode){ //点击左侧品名标签
        this.BrandActive = BrandName
        this.BrandCode = BrandCode
        this.currentBrandBatch=[]
        var params = {
          tableName:this.planTableData.tableName,
          field:'PlanStatus',
          fieldvalue:'已下发',
          limit:this.planTableData.limit,
          offset:this.planTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          console.log(res.data.data.rows)
          var arr=res.data.data.rows
          this.currentBrandBatch=arr.forEach((item, index) => {
            if(item.BrandName===this.BrandActive){
              this.currentBrandBatch.push(item)
              this.planTableData.data=this.currentBrandBatch
              this.planTableData.total = this.currentBrandBatch.length
            }else{
              this.planTableData.total = 0
            }
          })
        
        })
      },
       getScheduleTableData(){ //获取品名
        var that = this
        var params = {
          tableName: "ProductRule",
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            var arr=res.data.data.rows
            this.currentBrandBatch=arr.map((value, index) => {

            })
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
      TabCurrentChange(e){ //点击显示当前的tab行显示详细信息
        this.currentBatch=e
        this.$refs.multipleTable.clearSelection();
        this.$refs.multipleTable.toggleRowSelection(e)
      },
       handleSizeChange(limit){ //每页条数切换
        this.planTableData.limit = limit
        this.clickBrandTag(this.BrandActive,this.BrandCode)
      },
       handleCurrentChange(offset) { // 页码切换
        this.planTableData.offset = offset
        this.clickBrandTag(this.BrandActive,this.BrandCode)
      },
       handleSelectionChange(row){
        this.multipleSelection = row
      },
    }
  }
</script>

<style scoped>
 .container-col{
    clear: both;
    overflow: hidden;
    border:1px solid rgba(185,185,185,1);
    background:#fff;
    border-radius: 4px;
    padding: 15px;
    margin-bottom: 15px;
    height: 50px;
  }
  .pactive{
    background-color:rgba(211,237,239,1);
  }
</style>
