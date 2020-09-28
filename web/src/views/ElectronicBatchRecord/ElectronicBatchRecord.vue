<template>
  <el-row :gutter="15">
    <el-col :span="4" v-if="currentBatch">  
         <div class="platformContainer">
            <p class="marginBottom">选择要查询的品名</p>
            <el-input class="marginBottom" v-model="productName" placeholder="关键字搜索" @change="handleChangeProductName"></el-input>
            <el-tag class="marginBottom marginRight cursor-pointer" v-for="(item,index) in results" :key="index" v-bind:effect="item.BrandName===BrandActive?'dark':'plain'" @click="clickBrandTag(item.BrandName,item.BrandCode)">{{item.BrandName}}</el-tag>
          </div>
    </el-col>
    <el-col :span='20' v-if="currentBatch">
        <div class="platformContainer" v-if="currentBatch">
              <p>当前选择的品名：{{BrandActive}}</p>
        </div>
        <div class="platformContainer" v-if="currentBatch">
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
    <el-col :span='24' v-if="!currentBatch">
        <div class="platformContainer">
           <div v-for="(item, index) in inProcessList" :key="index" class="list-complete-item" :data-idd="item.ID" style="display:inline-block;marginRight:18px;cursor:pointer" @click='ClickPU(item.PUCode,index)'>
                    <div class="container-col" :class="{'pactive':PUActive===index}">
                      <span class="text-size-14">{{ item.PUName }}</span>
                    </div>
                    <i class="fa fa-arrow-right" style="vertical-align: top;margin-top: 10px;" v-if="index != inProcessList.length -1"></i>
            </div>
        </div>
    </el-col>
    <el-col :span='24' v-if="!currentBatch">
        <div>
          <el-button type="primary" @click="backTab" icon="el-icon-d-arrow-left" size='small'>返回上一级</el-button><el-button type="primary" icon="el-icon-folder-opened" size='small'>编辑保存</el-button>
        </div>
    </el-col>
    <el-col :span='24' v-if="!currentBatch">
        <div class="platformContainer marginTop">
          <table class="elementTable" cellspacing="1" cellpadding="0" border="0" v-html="filebyte">

          </table>
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
        currentBatch:true,//控制显示表格 boolen
        multipleSelection:[],
        currentBrandBatch:[],
        inProcessList:[],
        filebyte:'',
        BrandCode:"",
        PUActive:0,
      }
    },
    created(){
      this.getScheduleTableData()
    },
    methods:{
      ClickPU(PUCode,index){ //点击工艺展示电子批记录
        this.PUActive=index
        var params={
          PUCode:PUCode,
          BrandCode:this.BrandCode
        }
        this.axios.get('/api/batchmodelselect',{params:params}).then((res) => {
          if(res.data.code==='200'){
            if(res.data.message.length!==0){
              this.filebyte=res.data.message[0].Parameter
               $("body").on("click",$(".elementTable p"),function(){
                  $(this).attr("contenteditable","true")
                })
            }else{
              this.filebyte=''
            }
          }else{
             this.$message({
              type: 'error',
              message: '获取批记录文档失败'
            });
          }
        })
      },
        handleChangeProductName(queryString){ //左侧查询品名
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
          var arr=res.data.data.rows
          this.currentBrandBatch=arr.forEach((item, index) => {
            if(item.BrandName===this.BrandActive){
              this.currentBrandBatch.push(item)
              this.planTableData.data=this.currentBrandBatch
              this.planTableData.total = this.currentBrandBatch.length
            }else{
              this.planTableData.data=[]
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
      TabCurrentChange(row){ //点击显示当前的tab行显示详细信息
        this.currentBatch=false
        this.BrandCode = row.BrandCode
        this.getBrandProcessTableData(row.BrandName)
        this.$refs.multipleTable.clearSelection();
        this.$refs.multipleTable.toggleRowSelection(row)

      },
       handleSizeChange(limit){ //每页条数切换
        this.planTableData.limit = limit
        this.clickBrandTag(this.BrandActive,this.BrandCode)
      },
       handleCurrentChange(offset) { // 页码切换
        this.planTableData.offset = offset
        this.clickBrandTag(this.BrandActive,this.BrandCode)//批记录模板初始化
      },
       handleSelectionChange(row){
        this.multipleSelection = row
      },
       getBrandProcessTableData(BrandName){ //查询当前品名绑定的工序
        var that = this
        var params = {
          tableName: "ProductUnit",
          field:"BrandName",
          fieldvalue:BrandName,
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            function compare(property){
              return function(a,b){
                var value1 = a[property];
                var value2 = b[property];
                return value1 - value2;
              }
            }
            that.inProcessList = res.data.data.rows.sort(compare('Seq'))
            this.ClickPU(that.inProcessList[0].PUCode,0)
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      backTab(){ //返回上一级下发表格
        this.currentBatch=true
      }
    }
  }
</script>

<style scoped>
   .container-col{
    display: inline-block;
    clear: both;
    overflow: hidden;
    border:1px solid #228AD5;
    background:#fff;
    border-radius: 4px;
    padding: 0 15px;
    margin-bottom: 15px;
    margin-right: 10px;
    height: 40px;
    line-height: 40px;
    color: #000;
  }
  .pactive{
    background-color:#228AD5;
    color:#fff;
  }
</style>
