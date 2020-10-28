<template>
     <el-col :span='24' class="platformContainer">
           <div style="height:40px;fontSize:16px;fontWeight:700;">ERP同步计划</div>
              <el-table
                  :data="ERPTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  ref="batchmultipleTable"
                  style="width: 100%">
                  <el-table-column type="selection" width="55"></el-table-column>
                  <el-table-column v-for="item in ERPtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="ERPTableData.total"
                  :current-page="ERPTableData.offset"
                  :page-size="ERPTableData.limit"
                  @size-change="erpHandleSizeChange"
                  @current-change="erpHandleCurrentChange">
                  </el-pagination>
            </div>
        </el-col>
</template>

<script>
  export default {
    name: "ERPDataManage",
    data(){
      return{
          ERPTableData:{ //批次列表
            tableName:"product_plan",
            data:[],
            limit: 10,//当前显示多少条
            offset: 1,//当前处于多少页
            total: 0,//总的多少页
        },
        ERPtableconfig:[{prop:'ID',label:"id"},{prop:'BrandCode',label:'品名编码'},
        {prop:'BrandName',label:'品名名称'},{prop:'PlanNum',label:'编号'},{prop:'BrandType',label:'药品类型'},
        {prop:'PlanQuantity',label:'计划产值'},{prop:'Unit',label:'产值单位'},{prop:'PlanStatus',label:'状态'},{prop:'CreateTimeTime',label:'创建时间',width:180}],//批次列表
      }
    },
    mounted(){
      this.getERPData()
    },
    methods:{
      getERPData(){
        var params={
          tableName:this.ERPTableData.tableName,
          offset:this.ERPTableData.offset-1,
          limit:this.ERPTableData.limit,
        }
        this.axios('/api/CUID',{params:params}).then((res) => {
          if(res.data.code === "200"){
            var data = res.data.data
            this.ERPTableData.data = data.rows
            this.ERPTableData.total = data.total
          }
          },err=>{
            console.log("请求错误")
          })
      },
      erpHandleSizeChange(limit){
        this.ERPTableData.limit=limit
        this.getERPData()

      },
      erpHandleCurrentChange(offset){
        this.ERPTableData.offset=offset
        this.getERPData()
      }
    }
  }
</script>

<style scoped>

</style>
