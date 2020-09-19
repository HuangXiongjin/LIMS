<template>
    <div class="platformContainer" style="height:1040px;">
        <el-row>
          <el-col :span='24' class="marginBottom"><div style="fontSize:16px;fontWeight:700;">计划详情</div></el-col>
          <el-col :span='24' style="marginBottom:30px;">
            <el-row>
              <el-col :span='3'>
                <div style="paddingBottom:14px;">计划单号</div>
                <div>{{currentSBatch.PlanNum}}</div>
              </el-col>
              <el-col :span='13'>
                 <div style="paddingBottom:14px;">状态</div>
                <div>{{currentSBatch.PlanStatus}}</div>
              </el-col>
              <el-col :span='4'><el-button type="warning" plain >驳回计划</el-button></el-col>
              <el-col :span='4'><el-button type="success" plain>执行计划</el-button></el-col>
            </el-row>
          </el-col>
          <el-col :span='24' class="marginBottom"><div style="fontSize:16px;fontWeight:700;">基础信息</div></el-col>
          <el-col :span='24' style="marginBottom:30px;">
             <el-table
              :data="[currentSBatch]"
              size='small'
              style="width: 100%">
             <el-table-column v-for="item in tableconfig" :width='item.width'  :key='item.prop' :prop='item.prop' :label='item.label'></el-table-column>
            </el-table>
          </el-col>
          <el-col :span='24' class="marginBottom"><div style="fontSize:16px;fontWeight:700;">物料BOM</div></el-col>
          <el-col :span='24' class="marginBottom">
            <div class="marginBottom">
               <el-table
                  :data="zhuMaterial"
                  size='small'
                  highlight-current-row
                  @row-click="ClickCurrentTab"
                  style="width: 100%">
                  <el-table-column v-for="item in materialbomtable" :key='item.prop' :prop='item.prop' :label='item.label'></el-table-column>
                </el-table>
                 <div class="paginationClass">
                  <el-pagination background  layout="total, prev, pager, next, jumper"
                  :total="materialbom.total"
                  :current-page="materialbom.offset"
                  :page-size="materialbom.limit"
                  @current-change="mbhandleCurrentChange">
                  </el-pagination>
            </div>
            </div>
            <div style="fontSize:16px;fontWeight:700;" class="marginBottom">物料明细</div>
            <div class="marginBottom">
               <el-table
                  :data="fuMaterial"
                  size='small'
                  style="width: 100%">
                  <el-table-column v-for="item in materialinfotable" :key='item.prop' :prop='item.prop' :label='item.label'></el-table-column>
                </el-table>
                 <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="materialinfobom.total"
                  :current-page="materialinfobom.offset"
                  :page-size="materialinfobom.limit"
                  @current-change="mihandleCurrentChange">
                  </el-pagination>
            </div>
            </div>
          </el-col>
          <el-col :span='24' class="marginBottom"><div style="fontSize:16px;fontWeight:700;">计划进度</div></el-col>
          <el-col :span='24' class="marginBottom">
            <el-steps :active="1" align-center >
                <el-step  v-for="(item,index) in steps" :title="item.title" :key='index' :description="item.description">
                    <template slot="description" >
                        <span>{{item.startTime}}<br/>{{item.endTime}}</span>
                    </template>
                </el-step>
             </el-steps>
          </el-col>
        </el-row>
      </div>
</template>
<script>
export default {
    props:['currentSBatch'],
    data(){
        return {
            currentMaterial:'',
            zhuMaterial: [{
            MATCode: 'AF-JS',
            MATName: '黄芪',
            BatchPercentage:20,
            BatchSingleMATWeight:10,
            BatchTotalWeight:90
          }],
          fuMaterial: [{
            MATCode: '黄芪',
            MATName: 'HQrtyy1',
            Desc:'生长于高原',
            MATTypeID:19,
            MATBatchNo:'LF-JS'
          },{
            MATCode: '黄芪',
            MATName: 'HQrtyy1',
            Desc:'生长于洼地',
            MATTypeID:20,
            MATBatchNo:'LF-JS'
          }],
            materialbom:{ //物料BOM
                tableName:"MaterialBOM",
                data:[],
                limit: 5,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            materialinfobom:{ //物料明细表
                tableName:"Material",
                data:[],
                limit: 5,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            steps:[{title:'计划申请',startTime:'2020-09-09',endTime:"2020-09-10"},{title:'计划审批',startTime:'2020-09-11',endTime:"2020-09-12"},{title:'计划下发',startTime:'2020-09-13',endTime:"2020-09-14"}],
            tableconfig:[{prop:'BatchID',label:"批次号",width:'170'},{prop:'BrandName',label:'品名',width:'90'},{prop:'PlanStatus',label:'计划状态',width:'110'},{prop:'PlanBeginTime',label:'计划开始时间'},{prop:'PlanEndTime',label:'计划完成时间'}],
            materialbomtable:[{prop:'MATCode',label:"物料编码"},{prop:'MATName',label:'物料名称'},{prop:'BatchPercentage',label:'百分比'},{prop:'BatchSingleMATWeight',label:'投料单一重量'},{prop:'BatchTotalWeight',label:'投料批总重量'}],
            materialinfotable:[{prop:'MATCode',label:"物料编码"},{prop:'MATName',label:'物料名称'},{prop:'Desc',label:'物料描述'},{prop:'MATTypeID',label:'物料类型ID'},{prop:'MATBatchNo',label:'物料标识'}],

        }
    },
    methods:{
       getMaterialBom(BrandName){ //查询当前品名物料BOM
        var that = this
        var params = {
          tableName: this.materialbom.tableName,
          field:"BrandName",
          fieldvalue:BrandName,
          limit:this.materialbom.limit,
          offset:this.materialbom.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.materialbom.data = res.data.data.rows
            that.materialbom.total = res.data.data.total
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
      ClickCurrentTab(e){
        this.currentMaterial=e.MATName
        this.getMaterialInfo(this.currentMaterial)
      },
       getMaterialInfo(materialname){ //查询当前品名物料详情信息
        var that = this
        var params = {
          tableName: this.materialinfobom.tableName,
          field:"MATName",
          fieldvalue:materialname,//当前点击的物料名称
          limit:this.materialinfobom.limit,
          offset:this.materialinfobom.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.materialbom.data = res.data.data.rows
            that.materialbom.total = res.data.data.total
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
       mbhandleCurrentChange(offset) { // 物料BOM页码切换
        this.materialbom.offset = offset
        this.getMaterialBom(this.currentSBatch.BrandName)
      },
       mihandleCurrentChange(offset) { // 物料详情页码切换
        this.materialinfobom.offset = offset
        this.getMaterialInfo(this.currentMaterial)
      },
    }
}
</script>
<style scoped>

</style>