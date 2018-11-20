clear all;
'LOADING......'
kk_max=10;
iii_max=3;
jjj_max=5;
ii_max=kk_max*jjj_max;

for kk=0:kk_max-1
    m=strcat('appr_',int2str(kk),'.bmp');
    bw=imread(m,'bmp');
    
    for iii=0:iii_max-1
        for jjj=0:jjj_max-1
            bww=bw(iii*64+1:iii*64+64,jjj*64+1:jjj*64+64);
            p(:,iii*ii_max+jjj*kk_max+kk+1)=getFeature(bww);
            t(iii*ii_max+jjj*kk_max+kk+1)=kk;
        end
    end
end

'LOAD OK.'
t;
save E52PT p t;

clear all;
load E52PT p t;
for i=1:15
pr(i,1)=min(p(i,:));
pr(i,2)=max(p(i,:));
end

net=newff(pr,[60 1],{'logsig','purelin'},'traingdx','learngdm');
net.trainParam.epochs=2500;
net.trainParam.goal=0.001;
net.trainParam.show=100;
net.trainParam.lr=0.1;
net=train(net,p,t);
'TRAIN OK.'

save E52net net;

for times=0:1
    clear all;
    load E52net net;
    
    zzz=input('FileNO:','s');
    xxx=str2num(input('LineNo:','s'));
    yyy=str2num(input('colmNo:','s'));
    test=strcat('appr_',zzz,'.bmp');
    x=imread(test,'bmp');
    bw=x((xxx-1)*64+1:(xxx-1)*64+64,(yyy-1)*64+1:(yyy-1)*64+64);
    
    [pp,bwp]=getFeature(bw);
    
    [a,Pf,Af]=sim(net,pp);
    
    disp(a);
    a=round(a);
    disp(a);
    
    imshow(bwp);
end
    