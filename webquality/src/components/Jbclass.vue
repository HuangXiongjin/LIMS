<template>
    <div class="mgb24">
        <div style="textAlign:center;paddingBottom:10px;color:#139168;">鉴别</div>
        <div class="container">
            <p type="success" v-for="(item,index) in jbarr" :key="index" class="fontsz10 greenadd mgb10">
                {{item.value}}<el-button type="danger" icon="el-icon-delete" circle size='mini' class="mgl15" @click="Deljb(item.id)"></el-button>
                <el-button type="primary" icon="el-icon-edit" circle size='mini' @click="Editjb(item.id)"></el-button>
            </p>
            <el-button type="success" size='mini' icon="el-icon-plus" @click="showInputtxt" class="mgt14"></el-button>
        </div>
    </div>
</template>
<script>
export default {
    data(){
        return {
           jbarr:[],
           jbID:'',
           inputVisible:false,
           jbinput:'',//鉴别输入
           addEventdialogVisible: false,
           jbopt:'',//区分鉴别添加修改操作
        }
    },
    methods: {
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
        Editjb(ID){ //编辑鉴别
           this.inputVisible=true
           this.jbopt='修改'
           this.jbID=ID
        },
         showInputtxt(){ //点击右侧加号弹出输入框
            this.jbopt='添加'
            this.inputVisible=true
            this.jbinput=''
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
                this.jbarr=res.data.data[0]['鉴别']
            })
        },
        showInputContent(){ //鉴别添加修改的展示
            if(this.jbopt==='修改'){
                var params={
                ID:this.jbID,
                Discern:this.jbinput,
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
                Discern:this.jbinput,
                No:this.tabRowNo,
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
            this.getPostedjb()
            this.inputVisible=false
        },
    },
}
</script>
<style scoped>

</style>