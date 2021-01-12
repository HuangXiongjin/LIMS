<template>
   <el-row :gutter="20">
        <el-col :span='5'>
            <el-col class="container" style="height:600px;overflow:auto;">
                <div class="fontWet titl">样本分类</div>
                <div style="marginTop:20px;">
                <el-tree
                    :data="treeDom"
                    node-key="id"
                    default-expand-all
                    :expand-on-click-node="false"
                    :props="defaultProps"
                    @node-click='showTabInfo'>
                    <span class="custom-tree-node" slot-scope="{ node, data }">
                    <span>{{ node.label }}</span>
                        <span class="operations">
                            <i v-if="data.hasOwnProperty('children')" @click="() => append(node,data)" class="el-icon-plus greenadd fontsz10"></i><!--增加分组-->
                            <i v-if="!data.hasOwnProperty('children')" @click="() => deletes(node,data)" class="el-icon-delete redde fontsz10"></i><!--删除分组-->
                            <i v-if="!data.hasOwnProperty('children')" @click="() => rename(node,data)" class="el-icon-edit bledit fontsz10"></i><!--重命名分组-->
                        </span>
                    </span>
               </el-tree>
                </div>
            </el-col>
        </el-col>
        <el-col :span='14' class="container">
            <el-col :span='24' class="mgt24">
                <div class="fontWet titl mgb24" style="height:40px;lineHeight:30px;borderBottom:1px solid #ccc;">{{currentgoods}}</div>
                <el-table
                    :data="batchTableData.data"
                    size='small'
                    highlight-current-row
                    style="width: 100%"
                    @selection-change="handleSelectionChange"
                    @row-click='getPostedjb'>
                    <el-table-column type="selection" width="55"></el-table-column>
                    <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                    <el-table-column
                        fixed="right"
                        label="操作"
                        width="100">
                        <template slot-scope="scope">
                            <el-button @click="handleEdit(scope.row)" type="text" size="small" class="bledit">修改</el-button>
                            <el-button @click.native.prevent="handleDelete(scope.row)" type="text" size="small" class="redde">删除</el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <div class="paginationClass">
                    <el-pagination background  layout="total,sizes,prev, pager, next, jumper"
                    :total="batchTableData.total"
                    :current-page="batchTableData.offset"
                    :page-size="batchTableData.limit"
                    :page-sizes="[5,10,]"
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange">
                    </el-pagination>
                </div>
            </el-col>
            <el-col :span='24' style="textAlign:right;" class="mgt24">
                <el-button type="danger" size='mini' @click="delMaterial">删除</el-button>
                <el-button type="success" size='mini' @click="newMaterial">新增</el-button>
            </el-col>
        </el-col>
        <el-col :span='5'>
            <el-col class="container" style="height:600px;overflow:auto;">
                <div class="fontWet titl">检验项</div>
                <div style="marginTop:20px;">
                    <div class="mgb24">
                        <div style="textAlign:center;paddingBottom:10px;color:#139168;">鉴别</div>
                        <div class="container">
                            <p type="success" v-for="(item,index) in jbarr" :key="index" class="fontsz10 greenadd mgb10">
                                {{item.value}}&nbsp;&nbsp;&nbsp;&nbsp;<i class="el-icon-delete redde fsz14px cursor" @click="Deljb(item.id)"></i>&nbsp;&nbsp;
                                <i class="el-icon-edit bledit2 fsz14px cursor" @click="Editjb(item.id)"></i>
                            </p>
                            <el-button type="success" size='mini' icon="el-icon-plus" @click="showInputtxt('鉴别')" class="mgt14"></el-button>
                        </div>
                    </div>
                     <div class="mgb24">
                        <div style="textAlign:center;paddingBottom:10px;color:#139168;">检查</div>
                        <div class="container">
                             <p type="success" v-for="(item,index) in jcarr" :key="index" class="fontsz10 greenadd mgb10">
                                {{item.value}}&nbsp;&nbsp;&nbsp;&nbsp;<i class="el-icon-delete redde fsz14px cursor" @click="Deljb(item.id)"></i>&nbsp;&nbsp;
                                <i class="el-icon-edit bledit2 fsz14px cursor" @click="Editjb(item.id)"></i>
                            </p>
                            <el-button type="success" size='mini' icon="el-icon-plus" @click="showInputtxt('检查')" class="mgt14"></el-button>
                        </div>
                    </div>
                     <div class="mgb24">
                        <div style="textAlign:center;paddingBottom:10px;color:#139168;">性状</div>
                        <div class="container">
                            <p type="success" v-for="(item,index) in xzarr" :key="index" class="fontsz10 greenadd mgb10">
                                {{item.value}}&nbsp;&nbsp;&nbsp;&nbsp;<i class="el-icon-delete redde fsz14px cursor" @click="Deljb(item.id)"></i>&nbsp;&nbsp;
                                <i class="el-icon-edit bledit2 fsz14px cursor" @click="Editjb(item.id)"></i>
                            </p>
                            <el-button type="success" size='mini' icon="el-icon-plus" @click="showInputtxt('性状')" class="mgt14"></el-button>
                        </div>
                    </div>
                     <div class="mgb24">
                        <div style="textAlign:center;paddingBottom:10px;color:#139168;">含量测定</div>
                        <div class="container">
                            <p type="success" v-for="(item,index) in hlcdarr" :key="index" class="fontsz10 greenadd mgb10">
                                {{item.value}}&nbsp;&nbsp;&nbsp;&nbsp;<i class="el-icon-delete redde fsz14px cursor" @click="Deljb(item.id)"></i>&nbsp;&nbsp;
                                <i class="el-icon-edit bledit2 fsz14px cursor" @click="Editjb(item.id)"></i>
                            </p>
                            <el-button type="success" size='mini' icon="el-icon-plus" @click="showInputtxt('含量测定')" class="mgt14"></el-button>
                        </div>
                    </div>
                     <div class="mgb24">
                        <div style="textAlign:center;paddingBottom:10px;color:#139168;">微生物限度</div>
                        <div class="container">
                            <p type="success" v-for="(item,index) in wswarr" :key="index" class="fontsz10 greenadd mgb10">
                                {{item.value}}&nbsp;&nbsp;&nbsp;&nbsp;<i class="el-icon-delete redde fsz14px cursor" @click="Deljb(item.id)"></i>&nbsp;&nbsp;
                                <i class="el-icon-edit bledit2 fsz14px cursor" @click="Editjb(item.id)"></i>
                            </p>
                            <el-button type="success" size='mini' icon="el-icon-plus" @click="showInputtxt('微生物限度')" class="mgt14"></el-button>
                        </div>
                    </div>
                </div>
            </el-col>
        </el-col>
        <el-dialog
            title="添加新的节点"
            width="25%"
            class="add-event-dialog"
            :visible.sync="addEventdialogVisible"
            size="tiny">
            <el-form ref="addEventForm" :model="addEventForm">
                <el-form-item label="节点名称" prop="categoryName" >
                <el-input v-model="addEventForm.categoryName"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer" >
                <el-button @click="addEventdialogVisible=false">取 消</el-button>
                <el-button type="primary" @click="editconfirm">确 定</el-button>
            </span>
        </el-dialog>
        <el-dialog
            title="添加新的物料类信息"
            width="30%"
            class="add-event-dialog"
            :visible.sync="materialdialogVisible"
            size="tiny">
            <el-form ref="materialForm" :model="MaterialForm" label-width="80px">
                <el-form-item label="产品品名">
                    <el-input v-model="MaterialForm.Product"></el-input>
                </el-form-item>
                <el-form-item label="品名编码">
                    <el-input v-model="MaterialForm.Code"></el-input>
                </el-form-item>
                <el-form-item label="产品来源">
                    <el-input v-model="MaterialForm.Source"></el-input>
                </el-form-item>
                <el-form-item label="单位">
                    <el-input v-model="MaterialForm.Unit"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer" >
                <el-button @click="materialdialogVisible=false">取 消</el-button>
                <el-button type="primary" @click="PostMaterialInfo">确 定</el-button>
            </span>
        </el-dialog>
        <el-dialog
            :title="opt"
            width="25%"
            :visible.sync="inputVisible"
            size="tiny"
        >
        <el-form ref="addInput">
            <el-form-item label="节点名称">
                <el-input 
                type="textarea"
                autosize
                placeholder="请输入内容"
                v-model="jbinput"
                ></el-input>
            </el-form-item>
         </el-form>
         <span slot="footer" class="dialog-footer" >
            <el-button @click="inputVisible=false">取 消</el-button>
            <el-button type="primary" @click="showInputContent">确 定</el-button>
         </span>
        </el-dialog>
    </el-row>
</template>
<script>
var moment=require('moment')
export default {
    data(){
        return {
           jbarr:[],
           jcarr:[],
           xzarr:[],
           hlcdarr:[],
           wswarr:[],
           jbID:'',
           inputVisible:false,
           jbinput:'',//鉴别输入
           addEventdialogVisible: false,
           jbopt:'',//区分鉴别添加修改操作
           opt:'',//区分鉴别检查性状
           tabRowNo:'',//tab row 的No
           Product:'',
           addEventForm:{
            categoryName: '',
            },
           MaterialForm:{ //新增输入框绑定
            Product: '',
            Code:'',
            Type:'',
            Source:'',
            Unit:'',
            IntoTime:'',
            No:'',
            IntoUser:localStorage.getItem('Name'),
            AlterTime:moment(new Date()).format('YYYY-MM-DD HH:mm:ss'),
            AlterUser:localStorage.getItem('Name'),
            },
           materialdialogVisible:false, //新增物料信息卡片
           currentNodeData:{},//rename之后的保存
           currentParent:'',
           currentgoods:'',//当前点击的物类
           currentid:'1001', //当前树的id
           checkedRow:[],//勾选的多条
           batchTableData:{ //物料BOM
                data:[],
                limit: 5,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            batchtableconfig:[{prop:'Product',label:"产品品名"},{prop:'Code',label:'产品编码'},{prop:'Source',label:'来源'},{prop:'Type',label:'类型'},{prop:'Unit',label:'单位'},{prop:'IntoTime',label:'录入时间',width:'160'},{prop:'IntoUser',label:'录入人'},{prop:'AlterTime',label:'修改时间',width:'160'},{prop:'AlterUser',label:'修改人'},],//批次列表
            options: [{
                value: '选项1',
                label: '物料一'
                }, {
                value: '选项2',
                label: '物料二'
                }],
           treeDom: [],//渲染的树
           Action:'add',
           defaultProps: {
            children: 'children',
            label: 'label'
            }
        }
    },
    created(){
        this.getTreeDom()
        this.refreshTable()
    },
    methods: {
        Editjb(ID){ //编辑鉴别
           this.inputVisible=true
           this.jbopt='修改'
           this.jbID=ID
        },
        Deljb(ID){ //删除鉴别
           var params={
               ID:ID
           }
           this.axios.delete('/lims/QualityStandard',{params:params}).then((res) => {
               if(res.data.code=='1000'){
                this.$message({
                    type:'success',
                    message:'删除成功'
                })
                this.getPostedjb()
               }
           })
           
        },
        showInputtxt(opt){ //点击右侧加号弹出输入框
            this.opt=opt
            this.jbinput=''
            this.jbopt='添加'
            this.inputVisible=true
        },
        getPostedjb(row){ //获取已经上传的鉴别
           if(row==undefined){
                this.tabRowNo=this.tabRowNo
                this.Product=this.Product
           }else{
               this.tabRowNo=row.No,
               this.Product=row.Product
           }
            var params={
                No:this.tabRowNo
            }
            this.axios.get('/lims/QualityStandard',{params:params}).then((res) => {
                this.jbarr=res.data.data[0]['Discern']
                this.jcarr=res.data.data[0]['Inspect']
                this.xzarr=res.data.data[0]['Character']
                this.hlcdarr=res.data.data[0]['Content']
                this.wswarr=res.data.data[0]['Microbe']
                
            })
        },
        showInputContent(){ //鉴别添加修改的展示
            if(this.opt=='鉴别'){
              if(this.jbopt==='修改'){
                var params={
                    ID:this.jbID,
                    Data:this.jbinput,
                    Product:this.Product
                }
            this.axios.patch('/lims/QualityStandard',this.qs.stringify(params)).then((res) => {
                if(res.data.code=='1000'){
                     this.$message({
                        type:'success',
                        message:'修改成功'
                    })
                }
            })
            }else{
                 var params={
                    No:this.tabRowNo,
                    Data:this.jbinput,
                    Type:'Discern',
                    Product:this.Product
                }
            this.axios.post('/lims/QualityStandard',this.qs.stringify(params)).then((res) => {
                if(res.data.code=='1000'){
                    this.$message({
                        type:'success',
                        message:'添加成功'
                    })
                }
            })
            }
            }else if(this.opt=='检查'){
                if(this.jbopt==='修改'){
                var params={
                    ID:this.jbID,
                    Data:this.jbinput,
                    Product:this.Product
                }
            this.axios.patch('/lims/QualityStandard',this.qs.stringify(params)).then((res) => {
                if(res.data.code=='1000'){
                     this.$message({
                        type:'success',
                        message:'修改成功'
                    })
                }
            })
            }else{
                var params={
                    No:this.tabRowNo,
                    Data:this.jbinput,
                    Type:'Inspect',
                    Product:this.Product
                }
            this.axios.post('/lims/QualityStandard',this.qs.stringify(params)).then((res) => {
                if(res.data.code=='1000'){
                    this.$message({
                        type:'success',
                        message:'添加成功'
                    })
                }
            })
            }
            }else if(this.opt=='性状'){
                if(this.jbopt==='修改'){
                var params={
                    ID:this.jbID,
                    Data:this.jbinput,
                    Product:this.Product
                }
            this.axios.patch('/lims/QualityStandard',this.qs.stringify(params)).then((res) => {
                if(res.data.code=='1000'){
                     this.$message({
                        type:'success',
                        message:'修改成功'
                    })
                }
            })
            }else{
            var params={
                    No:this.tabRowNo,
                    Data:this.jbinput,
                    Type:'Character',
                    Product:this.Product
                }
            this.axios.post('/lims/QualityStandard',this.qs.stringify(params)).then((res) => {
                if(res.data.code=='1000'){
                    this.$message({
                        type:'success',
                        message:'添加成功'
                    })
                }
            })
            }
            }else if(this.opt=='含量测定'){
                if(this.jbopt==='修改'){
                var params={
                    ID:this.jbID,
                    Data:this.jbinput,
                    Product:this.Product
                }
            this.axios.patch('/lims/QualityStandard',this.qs.stringify(params)).then((res) => {
                if(res.data.code=='1000'){
                     this.$message({
                        type:'success',
                        message:'修改成功'
                    })
                }
            })
            }else{
             var params={
                    No:this.tabRowNo,
                    Data:this.jbinput,
                    Type:'Content',
                    Product:this.Product
                }
            this.axios.post('/lims/QualityStandard',this.qs.stringify(params)).then((res) => {
                if(res.data.code=='1000'){
                    this.$message({
                        type:'success',
                        message:'添加成功'
                    })
                }
            })
            }
            }else if(this.opt=='微生物限度'){
                if(this.jbopt==='修改'){
                var params={
                ID:this.jbID,
                Data:this.jbinput,
                Product:this.Product
            }
            this.axios.patch('/lims/QualityStandard',this.qs.stringify(params)).then((res) => {
                if(res.data.code=='1000'){
                     this.$message({
                        type:'success',
                        message:'修改成功'
                    })
                }
            })
            }else{
                var params={
                    No:this.tabRowNo,
                    Data:this.jbinput,
                    Type:'Microbe',
                    Product:this.Product
                }
            this.axios.post('/lims/QualityStandard',this.qs.stringify(params)).then((res) => {
                if(res.data.code=='1000'){
                    this.$message({
                        type:'success',
                        message:'添加成功'
                    })
                }
            })
            }
            }      
            this.getPostedjb()
            this.inputVisible=false
        },
        showTabInfo(obj,data,node){ //点击物料类展示对应的详细信息
        this.currentgoods = obj.label
        if(obj.hasOwnProperty('id')){
            this.currentid=obj.id
            var params={
                Code:this.currentid,
                PerPage:this.batchTableData.limit,
                Page:this.batchTableData.offset,
            }
            this.axios.get('/lims/QualityStandardCenter',{params:params}).then((res) => {
                if(res.data.code=='1000'){
                    this.batchTableData.data=res.data.data
                    this.batchTableData.total=res.data.total
                }
            })
        }
        },
        refreshTable(){ //刷新表格里面的数据
            var that=this
            var params1={
                Code:this.currentid,
                PerPage:this.batchTableData.limit,
                Page:this.batchTableData.offset,
            }
            that.axios.get('/lims/QualityStandardCenter',{params:params1}).then((res) => {
                if(res.data.code=='1000'){
                    that.batchTableData.data=res.data.data
                    that.batchTableData.total=res.data.total
                }
            })
        },
        getTreeDom(){ //初始化获取树结构
            this.axios.get('/lims/ClassifyTree').then((res) => {
                if(res.data.code==='1000'){
                    this.treeDom=res.data.data[0].children
                }
            })
        },
        handleEdit(row){ //表格编辑按钮
            this.MaterialForm.Product=row.Product
            this.MaterialForm.Code=row.Code
            this.MaterialForm.Source=row.Source
            this.MaterialForm.Unit=row.Unit
            this.MaterialForm.No=row.No
            this.materialdialogVisible=true
            this.Action='update'
        },
        handleDelete(row){ //表格删除按钮
            var arr=[]
            arr.push(row.ID)
            var params={
                ID:arr
            }
            this.axios.delete('/lims/QualityStandardCenter',{data:params}).then((res) => {
                if(res.data.code=='1000'){
                       this.$message({
                        type:'success',
                        message:'删除数据成功'
                    })
                    this.refreshTable()
                   }
            })
        },
        PostMaterialInfo(){ //发送录入的详细信息
            var that=this
            var params={
                ID:that.currentid,
                Product:that.MaterialForm.Product,
                Code:that.MaterialForm.Code,
                Type:that.currentgoods,
                Source:that.MaterialForm.Source,
                Unit:that.MaterialForm.Unit,
            }
            if(that.Action=='add'){
                params.Action='add'
                params.IntoTime=moment(new Date()).format('YYYY-MM-DD HH:mm:ss')
                params.IntoUser=localStorage.getItem('Name')
            }else{
                params.Action='update'
                params.AlterTime=moment(new Date()).format('YYYY-MM-DD HH:mm:ss')
                params.AlterUser=localStorage.getItem('Name')
                params.No=that.MaterialForm.No
            }
            that.axios.post('/lims/QualityStandardCenter',this.qs.stringify(params)).then((res) => { 
                if(res.data.code=='1000'){
                     that.$message({
                        type: 'success',
                        message: '操作成功'
                        });
                    //添加成功重新获取新的table
                     this.refreshTable()
                }else{
                   that.$message({
                        type: 'success',
                        message: '添加失败，请重试'
                        }); 
                }
                that.materialdialogVisible=false
            })
        },
        newMaterial(){ //命名弹出框
            this.materialdialogVisible=true
            this.MaterialForm={}
            this.Action='add'
        },
        handleSelectionChange(row){ //表格勾选触发
            this.checkedRow=row
        },
        delMaterial(){ //点击按钮删除
            var dels=[]
            if(this.checkedRow.length==0){
                this.$message({
                    type:'info',
                    message:'请先勾选表格里要删除的数据'
                })
            }else{
                dels=this.checkedRow.map((item) => {
                    return item.ID
                })
                var params={ID:dels}
                this.axios.delete('/lims/QualityStandardCenter',{data:params}).then((res) => {
                   if(res.data.code=='1000'){
                       this.$message({
                        type:'success',
                        message:'删除数据成功'
                    })
                    this.refreshTable()
                   }
                })
                
            }
        },
        append(node,data) { //添加节点
            this.currentParent=data.label
            var params={
                    ParentName:this.currentParent,
                    ChildrenName:'新增节点'
                }
                this.axios.post('/lims/ClassifyTree',this.qs.stringify(params)).then((res) => {
                    if(res.data.code=='1000'){
                        this.$message({
                            type:'success',
                            message:'添加节点成功'
                        })
                        this.getTreeDom()
                    }
                })
        },
        deletes(node,data){ //删除节点
            this.currentNodeData=data
            this.$confirm('确定要删除该节点吗？', '温馨提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                var params={
                    Code:this.currentNodeData.id,
                    ChildrenName:this.currentNodeData.label
                }
                this.axios.delete('/lims/ClassifyTree',{params:params}).then((res) => {
                    if(res.data.code=='1000'){
                        this.$message({
                          type: 'success',
                          message: '已删除'
                        });
                        this.getTreeDom()
                }
                })
            }).catch(() => {
                this.$message({
                type: 'info',
                message: '已取消删除'
                });
            });
        },
        rename(node,data){ //节点重命名
            this.currentParent=node.parent.data.label
            this.addEventdialogVisible=true
            this.currentNodeData=data
        },
        editconfirm(){ //节点命名修改确认
            if(this.addEventForm.categoryName!=''){
                this.currentNodeData.label=this.addEventForm.categoryName
                this.addEventdialogVisible=false
                var params={
                    ParentName:this.currentParent,
                    Code:this.currentNodeData.id,
                    ChildrenName:this.addEventForm.categoryName
                }
                this.axios.patch('/lims/ClassifyTree',this.qs.stringify(params)).then((res) => {
                    if(res.data.code=='1000'){
                        this.$message({
                            type: 'success',
                            message: '修改节点名称成功'
                            });
                       this.getTreeDom()
                    }else{
                        this.$message({
                            type:'error',
                            message:'修改节点失败'
                        })
                    }
                })
            }else{
                this.$message({
                    type:'error',
                    message:'节点名称不能为空'
                })
            }
        },
        handleSizeChange(limit){ //每页条数切换
            this.batchTableData.limit = limit
            this.refreshTable()
            
      },
        handleCurrentChange(offset) { // 页码切换
            this.batchTableData.offset = offset
            this.refreshTable()

        },
    },
}
</script>
<style scoped>
    .operations{
        margin-left: 30px;
        position: absolute;
        right: 4px;
    }
    .el-tree-node__content{
        position: relative;
    }
</style>