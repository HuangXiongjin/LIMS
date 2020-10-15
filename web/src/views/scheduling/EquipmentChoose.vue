<template>
    <el-row :gutter='15'>
        <el-col :span='8'>
            <div class="platformContainer" style="overflow:auto;">
                <div style="height:40px;fontSize:16px;fontWeight:700;">已下发的批次计划</div>
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
        <el-col :span='16'>
                <div class="platformContainer">
                    <div class="marginBottom"><span style="fontSize:16px;fontWeight:700;marginRight:30px;">当前选择的品名</span>{{currentBrandName}}</div>
                    <p class="marginBottom" style="fontSize:14px;fontWeight:700;">对应工艺段</p>
                    <div v-loading="loading" element-loading-text="数据加载中..." element-loading-spinner="el-icon-loading" style="height:60px;">
                        <div v-for="(item, index) in inProcessList" :key="index" class="list-complete-item" :data-idd="item.ID" style="display:inline-block;marginRight:18px;cursor:pointer" @click='getEquipmentList(index,item.eqList,item.PUCode,item.PUName)'>
                                <div class="container-col" :class='{"pactive":index===ActiveIndex}'>
                                    <span class="text-size-14">{{ item.PUName }}</span>
                                </div>
                        </div>
                    </div>
                </div>
                <div class="platformContainer">
                        <el-col :span='24' class="marginTop transfer">
                            <el-transfer v-model="selectedEquipment" :data="selectEquipment"  :titles="['可选设备', '已选设备']"  :button-texts="['剔除设备', '添加设备']">
                                <el-button class="transfer-footer" slot="right-footer" size="small" @click='SaveEq'>保存</el-button>
                            </el-transfer>
                        </el-col>
                </div>
        </el-col>
    </el-row>
</template>>
<script>
var moment=require('moment')
export default {
    data(){
        return {
             planTableData:{
                tableName:"PlanManager",
                data:[],
                limit: 10,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            inProcessList:[],
            currentBrandName:'',
            ActiveIndex:10,
            loading:false,
            selectedEquipment:[],
            selectEquipment:[],
            EQPCode:'',
            Id:'',//当前批次的ID
            PUCode:'',//当前的工艺段编码,
            PUName:'',//当前的工艺段名称
            tableconfig:[{prop:'BatchID',label:"批次号"},{prop:'PlanNum',label:'计划单号'},{prop:'BrandName',label:'品名'},{prop:'PlanStatus',label:'计划状态'}],

        }
    },
    created(){
        this.getBatchTable()
    },
    methods:{
        SaveEq(){
            var params={
                ID:this.Id,
                PUName:this.PUName,
                PUCode:this.PUCode,
                eqList:JSON.stringify(this.selectedEquipment)
            }
            console.log(this.selectedEquipment)
            console.log(JSON.stringify(this.selectedEquipment))
            console.log(typeof(JSON.stringify(this.selectedEquipment)))
            this.axios.post('/api/saveEQPCode',this.qs.stringify(params)).then((res) => {
                console.log(res)
            })
        },
        getEquipmentList(index,eqList,PUCode,PUName){ //点击工艺段
            this.ActiveIndex=index
            this.PUCode=PUCode
            this.PUName=PUName
            var newarr=[]
            eqList.forEach((item) => {
                if(item.isSelected){
                    newarr.push({key:item.EQPCode,label:item.EQPName+"(已选择)",disabled:false})
                }else{
                    newarr.push({key:item.EQPCode,label:item.EQPName,disabled:false})    
                }
                return {key:item.EQPCode,label:item.EQPName}
            })
            this.selectEquipment=newarr
        },
        handleSelectionChange(row){
            this.multipleSelection = row
        },
         TabCurrentChange(e){ //点击显示当前的tab行显示详细信息
            this.currentBrandName=e.BrandName
            this.Id=e.ID
            this.$refs.multipleTable.clearSelection();
            this.$refs.multipleTable.toggleRowSelection(e)
            this.getBrandProcess(e.BatchID,e.BrandCode)
        },
        handleSizeChange(limit){ //每页条数切换
            this.planTableData.limit = limit
            this.getBatchTable()
        },
        handleCurrentChange(offset) { // 页码切换
            this.planTableData.offset = offset
            this.getBatchTable()
        },
        getBatchTable(){ //初始获取已下发状态的批次
            var that=this
            var radiovalue = "已下发"
            var offset=this.planTableData.offset - 1
            var limit=this.planTableData.limit
            var api="/api/CUID?tableName=PlanManager&PlanStatus="+radiovalue+"&limit="+limit+"&offset="+offset
            this.axios.get(api).then(res => {
            if(res.data.code === "200"){
                console.log(res)
                var data = res.data.data
                that.planTableData.data = data.rows
                that.planTableData.total = data.total
            }
            },err=>{
            console.log("请求错误")
            })
        }, 
        getBrandProcess(BatchID,BrandCode){ //获取对应工艺段
            var that = this
            that.loading=true
            var params = {
                BatchID: BatchID,
                BrandCode:BrandCode
            }
            this.axios.get("/api/batchequimentselect",{
                params: params
            }).then(res => {
                console.log(res.data.data)
                if(res.data.code === "200"){
                function compare(property){
                    return function(a,b){
                    var value1 = a[property];
                    var value2 = b[property];
                    return value1 - value2;
                    }
                }
                that.inProcessList = res.data.data.processList.sort(compare('Seq'))
                that.loading=false
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