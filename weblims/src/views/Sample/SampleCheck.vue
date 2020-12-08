<template>
    <el-row :gutter='20'>
        <el-col :span='24' class="mgt24">
            <el-row>
                <el-col :span='3' class="mgr15 boxshadow">
                    <el-input
                        placeholder="类别/品名"
                        prefix-icon="el-icon-search"
                        v-model="searchObj.category">
                    </el-input>
                </el-col>
                <el-col :span='3' class="mgr15 boxshadow">
                    <el-select v-model="searchObj.goods" placeholder="物料类">
                        <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                        </el-option>
                    </el-select>
                </el-col>
                <el-col :span='3' class="mgr15 boxshadow">
                      <el-date-picker
                        v-model="searchObj.registrydate"
                        type="date"
                        placeholder="选择日期">
                      </el-date-picker>
                </el-col>
            </el-row>
        </el-col>
        <el-col :span='24' class="mgt24">
            <div class="container">
                <el-menu :default-active="'1'" class="bgwhite" mode="horizontal" @select="handleSelect">
                    <el-menu-item :index="'1'" style="height:46px;lineHeight:30px;">申请列表</el-menu-item>
                    <el-menu-item :index="'2'"  style="height:46px;lineHeight:30px;">申请通过清单</el-menu-item>
                </el-menu>
                <div class="mgt24" v-if="currentChoose==='1'">
                    <el-table
                    :data="batchTableData.data"
                    size='small'
                    highlight-current-row
                    style="width: 100%"
                    @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55"></el-table-column>
                    <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label'></el-table-column>
                    <el-table-column
                        fixed="right"
                        label="操作"
                        width="100">
                        <template slot-scope="scope">
                            <el-button @click="handlePass(scope.row)" type="text" size="small" class="bledit">通过</el-button>
                            <el-button @click.native.prevent="handleBack(scope.row)" type="text" size="small" class="redde">驳回</el-button>
                        </template>
                    </el-table-column>
                    </el-table>
                    <div class="paginationClass">
                        <el-pagination background  layout="total, prev, pager, next, jumper"
                        :total="batchTableData.total"
                        :current-page="batchTableData.offset"
                        :page-size="batchTableData.limit"
                        @size-change="handleSizeChange"
                        @current-change="handleCurrentChange">
                        </el-pagination>
                    </div>
                    <div style="textAlign:right;" class="mgt24">
                        <el-button type="danger" size='mini'>驳回</el-button>
                        <el-button type="success" size='mini' @click="mulBatchPass">批量审核通过</el-button>
                    </div>
                </div>
                <div class="mgt24" v-if="currentChoose==='2'">
                    <el-table
                    :data="batchTableData.data"
                    size='small'
                    highlight-current-row
                    style="width: 100%">
                    <el-table-column type="selection" width="55"></el-table-column>
                    <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label'></el-table-column>
                    </el-table>
                    <div class="paginationClass">
                        <el-pagination background  layout="total, prev, pager, next, jumper"
                        :total="batchTableData.total"
                        :current-page="batchTableData.offset"
                        :page-size="batchTableData.limit"
                        @size-change="handleSizeChange"
                        @current-change="handleCurrentChange">
                        </el-pagination>
                    </div>
                </div>
            </div>
        </el-col>
    </el-row>
</template>
<script>
export default {
    data(){

        return {
           checkedRow:[],
           searchObj:{
               category:'',
               registrydate:'',
               goods:'',
           },
            options: [{
                value: '选项1',
                label: '物料一'
                }, {
                value: '选项2',
                label: '物料二'
                }],
            currentChoose:'1',
            batchTableData:{ //物料BOM
                data:[{Specs:'60g/袋',CheckNumber:'BJJN1234',Name:'巴戟胶囊'},{Specs:'900g/袋',CheckNumber:'GHDGHH',Name:'复方斑蝥片'}],
                limit: 10,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            batchtableconfig:[{prop:'Specs',label:"规格"},{prop:'CheckNumber',label:'请验单号'},{prop:'Name',label:'品名'},{prop:'ProductNumber',label:'来料批号'},{prop:'Supplier',label:'供货单位'},{prop:'Number',label:'物料编码'},{prop:'Amount',label:'数量'},{prop:'Unit',label:'单位'},{prop:'CheckDate',label:'请验时间'}],//批次列表
        }
    },
    created(){
    },
    methods: {
        mulBatchPass(){ //多条数据审核通过
            if(this.checkedRow.length==0){
                this.$message({
                    type:'error',
                    message:'请选勾选要通过的数据'
                })
            }else{
                this.$confirm('此操作将审核通过该项, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
                }).then(() => {
                    this.$message({
                      type: 'success',
                      message: '审核通过'
                    });
                }).catch(() => {
                    this.$message({
                      type: 'info',
                      message: '已取消审核'
                    });   
                })
                }
        },
        handleSelectionChange(row){ //批量通过审核
            this.checkedRow=row
        },
        handleBack(row){ //驳回审核
            console.log(row)
        },
        handlePass(row){ //通过审核
            this.$confirm('此操作将审核通过该项, 是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
            }).then(() => {
                var params={
                CheckNumber:row.CheckNumber,
                VerifyName:localStorage.getItem('Name')
            }
            this.axios.post('https://yapi.baidu.com/mock/18229/CheckVerify',this.qs.stringify(params)).then((res) => {
                if(res.data.code=='1000'){
                    this.$message({
                      type: 'success',
                      message: '审核通过!'
                    });
                }
            })
            }).catch(() => {
            this.$message({
                type: 'info',
                message: '已取消审核'
            });          
            });
        },
        handleSelect(key) {
            this.currentChoose=key
        },
        handleSizeChange(limit){ //每页条数切换
            this.batchTableData.limit = limit
      },
        handleCurrentChange(offset) { // 页码切换
            this.batchTableData.offset = offset
        }
    },
}
</script>
<style scoped>

</style>