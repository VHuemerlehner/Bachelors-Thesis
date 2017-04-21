allFolders = dir('.\\melodies');

for j = 1:length(allFolders)
    
    tmpStruct = [];
    
    if allFolders(j).name(1) ~= '.'
        
        fprintf('Folder: %s\n', allFolders(j).name);
        
        foldName = allFolders(j).name;
        
        list = dir(sprintf('.\\melodies\\%s\\*.txt',foldName));
        
        for i = 1:length(list)
            tmpStruct = mergeMelody(foldName, list(i).name);
        end
        
    end
    
end